LAMBDA_DIR := lambda-code
ZIP_FILE := lambda_function_payload.zip

zip:
	cd $(LAMBDA_DIR) && zip -r ../$(ZIP_FILE) ./
