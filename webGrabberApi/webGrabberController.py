from playwright.async_api import async_playwright
import os

async def webGrabber():
    # Configuration
    downloadDir = "./downloads"
    url = "https://www2.fmc.gov/oti/"
    elementXpath = "//*[@id='buttonOTIListDownload']"
    print(f"\n\nWelcome to my Web Grabber..!! :) \n\n")
    # Ensure download directory exists
    os.makedirs(downloadDir, exist_ok=True)
    print(f"Creating absolute path for default download directory: {downloadDir}")
    downloadDirAbs = os.path.abspath(downloadDir)
    print(f"Absolute Download directory : {downloadDirAbs}\n")
    # checks the directory and deletes existing file
    print(f"Finding if we have existing files in the directory {downloadDirAbs}")
    for filename in os.listdir(downloadDirAbs):
        print(f"Checking file: {filename}")
        if filename.startswith("OTI") and (filename.endswith(".xlsx") or filename.endswith(".crdownload")):
            print(f"Existing file found: {filename}")
            os.remove(os.path.join(downloadDir, filename))
            print(f"File removed: {filename}\n")

    # Initialize webdriver
    async with async_playwright() as p:
        browser = await p.chromium.launch()  # Or p.firefox.launch() or p.webkit.launch()
        page = await browser.new_page()
        await page.goto(url)
        try:
            print(f"Visiting URL: {url}\n")
            button = page.locator(elementXpath)
            # wait for download to complete
            async with page.expect_download() as download_info:  # Essential step
                # click and trigger download
                print(f"Click operation on XPATH {button}\n")
                await button.click()
                download = await download_info.value  # Get the Download object

                # Get the suggested file name:
                suggested_filename = download.suggested_filename

                # Save the downloaded file:
                print(f"Downloading file: {suggested_filename}\n")
                download_path = f"{downloadDirAbs}/{suggested_filename}" # Specify the directory
                await download.save_as(download_path)
                print(f"File Name: {suggested_filename}\n")
                print(f"File downloaded to: {download_path}")
                return {"file_name": suggested_filename, "file_path": downloadDirAbs}

        except Exception as e:
            print(f"An error occurred: {e}\n")

        finally:
            # Close the browser (even if an error occurred)
            await browser.close()
