"""Module for uploading custom content"""

import inspect
import logging

from typing import Any, Dict, Sequence

from .base import handle_response, rate_limited
from .session import HexpySession

logger = logging.getLogger(__name__)


class ContentUploadAPI:
    """Class for working with Content Upload API.

    You may use the Content Upload endpoint to upload documents for analysis.
    In the past, users have uploaded survey responses, proprietary content,
    and other types of data not available in the Crimson Hexagon data library.
    To use this endpoint, please contact support and they will create a new custom content type for you.

    [Reference](https://apidocs.crimsonhexagon.com/reference#content-upload-1)

    # Example Usage

    ```python
    >>> from hexpy import HexpySession, ContentUploadAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> upload_client = ContentUploadAPI(session)
    >>> items = [
        {
          "title": "Example Title",
          "date": "2010-01-26T16:14:00",
          "author": "me",
          "url": "http://www.crimsonhexagon.com/post1",
          "contents": "Example content",
          "language": "en",
          "type": "Your_Assigned_Content_Type_Name",
          "geolocation": {
            "id": "USA.NY"
          }
        },
      ]
    >>> upload_client.upload(items)
    >>> session.close()
    ```
    """

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        self.TEMPLATE = session.ROOT + "content/"
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["batch_upload", "__init__"]:
                setattr(
                    self, name, rate_limited(fn, session.MAX_CALLS, session.ONE_MINUTE)
                )

    def upload(self, data: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        """Upload list of document dictionaries to Crimson Hexagon platform.

        If greater than 1000 items passed, reverts to batch upload.
        # Arguments
            data: list of document dictionaries  to upload.
        """
        if len(data) <= 1000:
            return handle_response(
                self.session.post(self.TEMPLATE + "upload", json={"items": data})
            )
        else:
            logger.info("More than 1000 items found.  Uploading in batches of 1000.")
            return self.batch_upload(data)

    def batch_upload(self, data: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch upload list of document dictionaries to Crimson Hexagon platform.

        # Arguments
            data: list of document dictionaries to upload in batches of 1000.
        """
        batch_responses = {}
        for batch_num, batch in enumerate(
            [data[i : i + 1000] for i in range(0, len(data), 1000)]
        ):
            response = self.upload(batch)
            logger.info(f"Uploaded batch number: {batch_num}")
            batch_responses[f"Batch {batch_num}"] = response
        return handle_response(batch_responses)

    def custom_field_upload(
        self, document_type: int, batch: int, data: Sequence[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Upload content via the API w/ custom fields support.

        # Arguments
            document_type: Integer, The id of the document type to which the uploading docs will belong.
            batch: Integer, The id of the batch to which the uploading docs will belong.
            data: list of document dictionaries  to upload.
        """
        return handle_response(
            self.session.post(
                self.TEMPLATE + "upload",
                params={"documentType": document_type, "batch": batch},
                json={"items": data},
            )
        )

    def delete_content_batch(
        self, document_type: int, batch: int, data=Dict[str, Any]
    ) -> Dict[str, Any]:
        """Delete batch content via the API.

        # Arguments
            * documentType: Integer, The id of the document type to delete documents from.
            * batch: String, The id of the document batch to delete.
        """
        return handle_response(
            self.session.post(
                self.TEMPLATE + "delete",
                params={"documentType": document_type, "batch": batch},
                json=data,
            )
        )

    def delete_content(
        self, document_type: int, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Delete content via the API.

        # Arguments
            * documentType: Integer, The id of the document type to delete documents from.
        """
        return handle_response(
            self.session.post(
                self.TEMPLATE + "delete",
                params={"documentType": document_type},
                json=data,
            )
        )

    def delete_content_source(
        self, document_type: int, remove_results: bool
    ) -> Dict[str, Any]:
        """Content Source deletion.

        # Arguments
            * documentType: Integer, The id of the document type to delete/
            * removeResults: Boolean, If true, removes the results associated with the documentType.
        """
        return handle_response(
            self.session.delete(
                self.TEMPLATE + "sources",
                params={"documentType": document_type, "removeResults": remove_results},
            )
        )

    def create_content_source(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Content Source creation."""
        return handle_response(self.session.post(self.TEMPLATE + "sources", json=data))

    def list_content_sources(self, team_id: int) -> Dict[str, Any]:
        """
        Content Source list.

        # Arguments
            * team: Integer, The id of the team to which the listed content sources belong.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "sources/list", params={"team": team_id})
        )
