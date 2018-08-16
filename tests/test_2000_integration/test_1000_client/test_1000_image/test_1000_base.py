import myutils
from myutils import pytest

@pytest.fixture
def app():
    from myutils.client.image import App
    return App.Load()
    
@pytest.fixture
def files_dir():
    from os import path

    return path.join(
        path.dirname(
            path.abspath(__file__)
        ),
        'files'
    )

@pytest.fixture
def tmp_dir():
    return myutils.test_mktmpdir(
        'myutils_client_images'
    )

@pytest.mark.parametrize(
    'png_fname,resample,width,height,ratio,error', [
    ('logo.png', 'AntiAlias', 128, None,1, None),
    ('logo.png', 'CUBIC', 64, None,2, None),
    ('logo.png', 'linear', 32, None,0, ValueError) # raises ValueError
])
def test_resize_image_png(
    app, files_dir, tmp_dir, 
    png_fname, resample, width, height, ratio,
    error
):
    from PIL import Image
    from os import path

    src_path = path.join(
        files_dir,
        png_fname
    )

    dst_path = path.join(
        tmp_dir,
        f'resize_img_png-{resample}-{width}-{height}-{ratio}-{png_fname}'
    )

    if error is not None:
        with pytest.raises(error):
            img = app.resizeImagePNG(
                src_path,
                dst_path,
                width,
                resample=resample,
                height=height,
                ratio=ratio
            )
        return

    else:
        img = app.resizeImagePNG(
            src_path,
            dst_path,
            width,
            resample=resample,
            height=height,
            ratio=ratio
        )

    assert isinstance(img, Image.Image)
    
    w, h = img.size

    assert w == width
    if not height:
        height = width * ratio
    assert h == height