build-QRUtilLayer:
	echo "Building layer..."
	mkdir -p $(ARTIFACTS_DIR)/python
	pip3 install -r requirements.txt -t $(ARTIFACTS_DIR)/python
	pip3 install --upgrade Pillow
	cp -R python/* $(ARTIFACTS_DIR)/python/