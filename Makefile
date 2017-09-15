LAMBDA_DIR := lambda-code
ZIP_FILE := lambda_function_payload.zip

zip:
	if [ -f "$(ZIP_FILE)" ]; then \
		rm $(ZIP_FILE); fi
	cd $(LAMBDA_DIR) && zip -r ../$(ZIP_FILE) ./
