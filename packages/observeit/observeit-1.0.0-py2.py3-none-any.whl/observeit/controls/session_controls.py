"""ObserveIT Recording APIs"""

import datetime
import logging
import os
import shutil
import tempfile
import traceback
from observeit.decorators import login_auth_only

LOG = logging.getLogger(__name__)


@login_auth_only
def start_recording(client, endpoint_name, tag_name, application_server,
                    login=None):
    # use the application server
    raise NotImplementedError()


@login_auth_only
def stop_recording(client, endpoint_name, application_server, login=None):
    # use the application server
    raise NotImplementedError()


@login_auth_only
def delete_recording(client, tag_name):
    raise NotImplementedError()


def export_session(client, session_id, dest_dir=""):
    """Save all session screenshots to directory as png files"""
    path, image_list = _download_screenshots(client, session_id, dest_dir=dest_dir)
    return path
# end export_session


def _download_screenshots(client, session_id, dest_dir=""):
    """Save all screenshots to a directory"""
    url = "activity/sessions/%s/events" % session_id
    image_list = []
    try:
        response = client.make_request(url,  headers={"accept": "application/json"})
        events = response.json().get("data", [])
        headers = {"Accept": "image/png"}
        path = dest_dir or session_id
        if events and not dest_dir:
            os.mkdir(path)
        for event in events:
            href = event.get("ui", {}).get("links", {}).get("screenshot", {}).get("href", None)
            LOG.debug("Got screenshot href: %s", href)
            if href:
                img_resp = client.make_request(href, headers=headers)
                filename = os.path.join(path, event["id"] + ".png")
                with open(filename, 'wb') as f:
                    for chunk in img_resp:
                        f.write(chunk)
                image_list.append({"path": filename,
                                   "metadata": event})
    except (OSError, IOError) as e:
        LOG.error("Erroring storing session data")
        LOG.debug(traceback.format_exc())
        raise
    except Exception as e:
        LOG.error("Failed to get events from ObserveIT!")
        LOG.debug(traceback.format_exc())
        raise
    return path, image_list
# end _download_screenshots


def _format_metadata(metadata):
    """pretty print useful metadata from json"""
    windows = metadata.get("ui", {}).get("windows", [])
    windows = windows[0] if windows else {}
    timestamp = metadata.get("createdAt", "N/A")
    ts = timestamp.replace("Z", "GMT")
    ms = int(ts[-6:-3])
    ts_format = "%Y-%m-%dT%H:%M:%S.%f%Z"
    dt = datetime.datetime.strptime(ts, ts_format)
    dt + datetime.timedelta(minutes=int(metadata["timezoneOffset"]))
    adjusted_timestamp =  dt.isoformat()
    metadata_list = ["Application Name:",
                     "  " + metadata.get("process", {}).get("applicationName", "N/A"),
                     "",
                     "Window Title:",
                     "  " + windows.get("windowTitle", "N/A"),
                     "",
                     "Site Name:",
                     "  " + windows.get("siteName", "N/A"),
                     "",
                     "UTC Timestamp:",
                     "  " + timestamp,
                     "",
                     "Local Agent Timestamp:",
                     "  " + adjusted_timestamp,
                     "",
                     "ID:",
                     "  " + metadata.get("id", "N/A")]
    return metadata_list
# end _format_metadata


def make_video(client, session_id, dest_dir=""):
    """Create a video from screenshots and metadata"""
    import cv2
    import numpy as np

    directory_name = None
    try:
        directory_name = tempfile.mkdtemp()
        image_path, image_list = _download_screenshots(client, session_id,
                                                       dest_dir=directory_name)
        if not image_list:
            raise RuntimeError("No screenshots found")

        # Determine the width and height from the first image
        frame = cv2.imread(image_list[0]["path"])
        cv2.imshow('video', frame)
        height, width, channels = frame.shape

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
        filename = session_id + ".mp4"
        output = os.path.join(dest_dir, filename) if dest_dir else filename
        text_width = 500
        out = cv2.VideoWriter(output, fourcc, 0.5, (width + text_width, height))
        font = cv2.FONT_HERSHEY_SIMPLEX

        for image in image_list:
            # Create a black image with white text
            text_img = np.zeros((height, text_width + width, 3), dtype=np.uint8)
            metadata = _format_metadata(image["metadata"])
            for i, line in enumerate(metadata):
                cv2.putText(text_img, line, (20, 90 + (27 * i)), font, 0.5,
                            (255, 255, 255), 1, cv2.LINE_AA)
            screenshot = cv2.imread(image["path"])
            text_img[:, text_width:text_width + width] = screenshot
            out.write(text_img)  # Write out frame to video

        # Release everything if job is finished
        out.release()
        cv2.destroyAllWindows()
    finally:
        if directory_name:
            shutil.rmtree(directory_name)

    return output
# end make_video
