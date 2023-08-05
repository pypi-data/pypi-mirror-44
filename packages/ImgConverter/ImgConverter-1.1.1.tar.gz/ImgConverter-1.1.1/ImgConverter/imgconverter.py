import os
from shutil import rmtree
from pathlib import Path
from tempfile import mkdtemp
from PIL import Image
from psdconvert import ConvertPSD
from pdf.convert import pdf2img


def jpg2png(source, destination):
    """Convert a JPG image to a PNG image."""
    assert Path(source).suffix == '.jpg'
    assert Path(destination).suffix == '.png'

    with Image.open(source) as im:
        im.save(destination)
    return destination


class Convert2Image:
    def __init__(self, dst_directory=None, convert_to='png', ignored_types=None):
        """Convert a variety of file formats to images."""
        self._dst_dir = dst_directory
        self._dst_ext = '.' + convert_to.strip('.')
        self.ignored_types = self._set_ignored_types(ignored_types)
        self.tempdir = None

    def cleanup(self):
        rmtree(self.tempdir)

    @staticmethod
    def _set_ignored_types(ignored_types):
        """Create list of ignored file types"""
        if isinstance(ignored_types, list):
            return ['.' + t.strip('.') for t in ignored_types]
        elif isinstance(ignored_types, str):
            return ['.' + ignored_types.strip('.')]
        else:
            return [None]

    @staticmethod
    def _get_name_ext(source):
        """
        Get file name and file extension from a source file

        :param source: A file path
        :return: file_name, file_ext
        """
        s = Path(os.path.basename(source))
        # Source file name without extension and file extension tup
        return s.stem, s.suffix

    def _get_target(self, src_name):
        """
        Retrieve the target file_path

        Returns either a tempfile in a tempdir or a concatenated
        file path in the same directory as the source file
        """
        if self._dst_dir and os.path.isdir(self._dst_dir):
            # Concatenate destination
            return os.path.join(self._dst_dir, src_name + self._dst_ext)

        else:
            # Create a temporary destination
            if self.tempdir is None:
                self.tempdir = mkdtemp()
            return os.path.join(self.tempdir, src_name + self._dst_ext)

    def get_output(self, source):
        """
        Get the output file path for a source file to-be converted

        :param source: Source file path
        :return: Destination file path
        """
        src_name, src_ext = self._get_name_ext(source)
        return self._get_target(src_name)

    def convert(self, source):
        """Convert a .jpg, .psd, .pdf or .png to another format"""
        # Source file name without extension and file extension tup
        src_name, src_ext = self._get_name_ext(source)

        # Target file path
        target = self._get_target(src_name)

        # No conversion needed
        if src_ext == self._dst_ext:
            return [source]

        # PSD ---> PNG
        elif src_ext == '.psd' and src_ext not in self.ignored_types:
            return [ConvertPSD(source).save(target)]

        # PDF ---> PNG
        elif src_ext == '.pdf' and src_ext not in self.ignored_types:
            return pdf2img(source, output=target)

        # JPG ---> PNG
        elif src_ext == '.jpg' and src_ext not in self.ignored_types:
            return [jpg2png(source, target)]

        # Cannot convert this file type
        else:
            print('Cannot convert', source)
            return None
