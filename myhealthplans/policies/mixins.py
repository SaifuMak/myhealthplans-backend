from django.db import models
from myhealthplans.const import R2_PUBLIC_URL
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class R2PublicURLMixin(models.Model):
    """
    Automatically sets public URLs for multiple file fields after saving.

    Example usage:
        file_url_map = {
            "aadhar": ("aadhar_public_url", "documents/aadhar/"),
            "pan": ("pan_public_url", "documents/pan/"),
            "document": ("document_public_url", "documents/policies/"),
        }
    """

    file_url_map = {}  # define this in your model (see example below)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save instance and automatically generate public URLs
        for all file fields defined in file_url_map.
        """
        # First, save normally to ensure files are uploaded
        super().save(*args, **kwargs)

        updated_fields = []

        for file_field_name, (url_field_name, path_prefix) in self.file_url_map.items():
            try:
                file_field = getattr(self, file_field_name, None)
                if not file_field:
                    continue

                filename = getattr(file_field, "name", None)
                if not filename:
                    continue  # skip if not uploaded yet

                # Normalize the filename (remove duplicate prefix if needed)
                if filename.startswith(path_prefix):
                    filename = filename[len(path_prefix):]

                new_url = f"{R2_PUBLIC_URL}{path_prefix}{filename}"

                # Update only if value changed
                if getattr(self, url_field_name) != new_url:
                    setattr(self, url_field_name, new_url)
                    updated_fields.append(url_field_name)

            except ClientError as e:
                logger.warning(f"Failed to build public URL for {file_field_name}: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error processing {file_field_name}: {e}")

        # Save only updated fields (to avoid recursion)
        if updated_fields:
            super().save(update_fields=updated_fields)
