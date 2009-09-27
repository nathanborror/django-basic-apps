from django import template
from django.conf import settings
register = template.Library()


# Useful functions
def _get_path_from_url(url, root=settings.MEDIA_ROOT, url_root=settings.MEDIA_URL):
    """ make filesystem path from url """
    import os
    if url.startswith(url_root):
        url = url[len(url_root):]       # strip media root url
    return settings.MEDIA_ROOT + url


# Tags
@register.filter
def thumbnail(url, size='200x200'):
    """
    Given a URL (local or remote) to an image, creates a thumbnailed version of the image, saving
    it locally and then returning the URL to the new, smaller version. If the argument passed is a
    single integer, like "200", will output a version of the image no larger than 200px wide. If the
    argument passed is two integers, like, "200x300", will output a cropped version of the image that
    is exactly 200px wide by 300px tall.

    Examples:

    {{ story.leadphoto.url|thumbnail:"200" }}
    {{ story.leadphoto.url|thumbnail:"300x150" }}

    """
    import Image
    import os
    import urllib

    original_url = url

    # First, find the image, either via local file path or http.
    filename = os.path.join(settings.MEDIA_ROOT, url)

    if url.startswith('http://') or url.startswith('https://'):
        # If it's a remote image, download it and save it locally. This expects a
        # directory called downloaded/ in your MEDIA_ROOT
        download_filename = url.rsplit('/', 1)[1]                                         # Filename of image
        full_image_path = '%sdownloaded/%s' % (settings.MEDIA_ROOT, download_filename)    # Local filesystem path where image should be saved
        local_image_url = '%sdownloaded/%s' % (settings.MEDIA_URL, download_filename)     # URL to local copy of image

        if not os.path.exists(full_image_path):
            unsized_image = urllib.urlretrieve(url)                                         # Fetch original image
            unsized_image = Image.open(unsized_image[0])                                    # Load the fetched image
            local_image = unsized_image.save(full_image_path)                               # Save the resized image locally

        url = local_image_url
        remote_image = True
    else:
        # If it's a local image, note it and move on.
        remote_image = False

    # Define the thumbnail's filename, file path, and URL.
    try:
        basename, format = url.rsplit('.', 1)
    except ValueError:
        return os.path.join(settings.MEDIA_URL, url)
    thumbnail = basename + '_t' + size + '.' +  format
    thumbnail_filename = _get_path_from_url(thumbnail)
    thumbnail_url = thumbnail

    # Find out if a thumbnail in this size already exists. If so, we'll not remake it.
    if not os.path.exists(thumbnail_filename):
        # The thumbnail doesn't already exist. Log a message that we are resizing.

        # Open the image.
        try:
            image = Image.open(_get_path_from_url(url))
        except IOError:
            return os.path.join(settings.MEDIA_URL, url)

        # Make a copy of the original image so we can access its attributes, even
        # after we've changed some of them.
        original_image = image.copy()

        # Find the size of the original image.
        original_width = original_image.size[0]
        original_height = original_image.size[1]

        # Parse the size argument into integers.
        try:
            # See if both height and width exist (i.e. "200x100")
            desired_width, desired_height = [int(x) for x in size.split('x')]
            new_size = (desired_width, desired_height)
            # Flag this image for cropping, since we want an explicit width AND height.
            crop = True
        except ValueError:
            # If only one exists ( i.e. "200"), use the value as the desired width.
            if size[0] == 'x':
                desired_height = int(size[1:])
                new_size = (original_width, desired_height)
                crop = False
            else:
                desired_width = int(size)
                new_size = (desired_width, original_height)
                crop = False

        # If we are to crop this image, we'll thumbnail it, and then figure out the proper crop area
        # Crops are done from the center of the image.
        if crop:
            if (original_height / (original_width / float(desired_width))) < desired_height:
                image.thumbnail((original_width, desired_height), Image.ANTIALIAS)
            else:
                image.thumbnail((desired_width, original_height), Image.ANTIALIAS)

            if (image.size[0] >= desired_width) and (image.size[1] >= desired_height):
                left = (image.size[0] - desired_width) / 2
                top  = (image.size[1] - desired_height) / 2
                right = left + desired_width
                bottom = top + desired_height
                cropped_image = image.crop((left, top, right, bottom))
                image = cropped_image
        else:
            # If we are not to crop this image, simply thumbnail it down to the desired width.
            image.thumbnail(new_size, Image.ANTIALIAS)

        # Finally, save the image.
        try:
            image.save(thumbnail_filename, image.format, quality=85)
        except KeyError:
            return ''

    # And return the URL to the new thumbnailed version.
    return os.path.join(settings.MEDIA_URL, thumbnail_url)