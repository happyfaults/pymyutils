from .. import Interactor, Factory

class Factory(Factory):
    pass

class App(Interactor):
    
    FactoryType = Factory.Default

    def resizeImagePNG(self, 
        src_path, 
        dst_path, 
        width, 
        height=None, 
        ratio=1, 
        resample='ANTIALIAS'
    ):
        from PIL import Image

        # resample mode
        rtype = getattr(Image, resample.upper(), None)
        if not isinstance(rtype, int):
            raise ValueError(
                f'Unknowm Image resample type: {resample}'
            )

        img = Image.open(src_path).convert('RGBA')
        img.load()

        if not height:
            height = width * ratio
            if not height:
                raise ValueError('Resize image height cannot be 0')
        
        bands = [
            b.resize(
                (width, height), 
                rtype
            ) 
            for b in img.split()
        ]
        
        # merge the channels after individual resize
        img = Image.merge(
            'RGBA', 
            bands
        )

        img.save(dst_path, format='png')

        return img
