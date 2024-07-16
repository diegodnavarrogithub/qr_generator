build-QRUtilLayer:
	echo "Building layer..."
	echo pwd
	echo ls
	mkdir -p $(ARTIFACTS_DIR)/python
	pip3 install -r requirements.txt -t $(ARTIFACTS_DIR)/python
	cp -R python/* $(ARTIFACTS_DIR)/python/