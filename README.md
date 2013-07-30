rghost-uploader
===============

Upload files to RGhost http://rghost.net/ from comand line

    $ rghost.py --tags="picture nature" \
                     --description="Lucy in the sky with diamonds" \
                     --removal_code="remove_later" \
                     --password="secret" \
                     --lifespan=1 \
                     --public="0" \
                     test.txt
    http://rghost.ru/private/47783143/2d2573410be063a1f588e63cfe9b4a6a
    
Or simplier:

	$ rghost.py test.txt 2.txt
	http://rghost.ru/private/47783374/c5a1706ba325f877b8e2dbe81f769d02
	http://rghost.ru/private/47783376/bf9b418fe18ad15d35813f0afb174d13