import os, asyncio, logging
from azure.storage.blob import BlockBlobService
from azure.common import AzureMissingResourceHttpError
from __app__.AppSettings.AppSettings import appSettings

class StorageAccountHelper:
	def __init__(self):
		self.firstTime = True
		if appSettings.STORAGE_ACCOUNT_NAME and appSettings.STORAGE_ACCOUNT_KEY:
			self.blob_service = BlockBlobService(account_name=appSettings.STORAGE_ACCOUNT_NAME, account_key=appSettings.STORAGE_ACCOUNT_KEY)
		else:
			raise Exception('Failed to read storage account name and key values from configurations')

	async def downloadFile(self, blobname, destpath=None):
		writepath = os.path.join(os.getcwd(), os.path.normpath('/'.join(blobname.split("/")[:-1])))
		fileName = blobname.split("/")[-1]
		if destpath:
			writepath = os.path.join(os.getcwd(), os.path.normpath(destpath))
		try:
			os.makedirs(writepath)
		except:
			pass
		try:
			self.blob_service.get_blob_to_path(appSettings.STORAGE_ACCOUNT_CONTAINER_NAME, blobname, os.path.join(writepath, fileName))
			logging.info("Downloaded file {0} to path {1}".format(blobname, writepath))
		except AzureMissingResourceHttpError as e:
			logging.error("File {0} not found on blob".format(blobname), exc_info=True)
	
	async def uploadFile(self, srcfilepath, destfilepath):
		self.blob_service.create_blob_from_path(appSettings.STORAGE_ACCOUNT_CONTAINER_NAME, destfilepath, srcfilepath)