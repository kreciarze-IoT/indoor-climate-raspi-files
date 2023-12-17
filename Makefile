upload:
	zip -r src.zip src
	scp src.zip krecik@rpi:~/indoor-climate-raspi-files
	rm src.zip
	ssh krecik@rpi 'cd indoor-climate-raspi-files && rm -r src && unzip src.zip && rm src.zip'
