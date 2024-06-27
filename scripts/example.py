import os
import time
import argparse
import logging
import subprocess
import undetected_chromedriver as uc
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CertificateLogger')

class CertificateInstaller:
    def __init__(self, cert_name, cert_password):
        self.cert_name = cert_name
        self.cert_password = cert_password or ''
        self.cert_file_path = f'/certs/{cert_name}.pfx' if cert_name else None

    def install_certificate(self):
        if not self.cert_file_path:
            logger.info('No certificate name provided, skipping certificate installation.')
            return
        try:
            logger.info(f'Installing certificate from {self.cert_file_path}')
            result = subprocess.run([
                'pk12util',
                '-i', self.cert_file_path,
                '-d', 'sql:/root/.pki/nssdb',
                '-W', self.cert_password
            ], capture_output=True, text=True, check=True)
            if result.stdout.strip():
                logger.info(result.stdout.strip())
            logger.info('Certificate installed successfully.')
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to install certificate: {e}', exc_info=True)
            if e.stdout and e.stdout.strip():
                logger.error(e.stdout.strip())
            if e.stderr and e.stderr.strip():
                logger.error(e.stderr.strip())

class ChromeDriverSetup:
    def __init__(self, cert_name):
        self.cert_name = cert_name
        self.driver = None

    def start_driver(self):
        options = uc.ChromeOptions()
        user_agent = UserAgent().chrome
        options.add_argument(f'user-agent={user_agent}')
        profile_directory = f"./{self.cert_name}" if self.cert_name else "./default_profile"
        current_directory = os.path.dirname(os.path.abspath(__file__))
        download_directory = os.path.join(current_directory, "downloads")
        prefs = {
            'download.default_directory': download_directory,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'plugins.always_open_pdf_externally': True
        }
        options.add_experimental_option('prefs', prefs)
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
        self.driver = uc.Chrome(user_data_dir=profile_directory,
                                options=options,
                                driver_executable_path="/usr/lib/chromium/chromedriver",
                                headless=False,
                                use_subprocess=False)
        self.driver.maximize_window()
        logger.info('Chrome driver started successfully.')

    def import_certificate_check(self):
        try:
            logger.info('Navigating to chrome://settings/certificates to check certificate import.')
            self.driver.get("chrome://settings/certificates")
        except Exception as e:
            logger.error(f"An error occurred during certificate import check: {e}", exc_info=True)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logger.info('Chrome driver closed.')

def main(cert_name, cert_password):
    cert_installer = CertificateInstaller(cert_name, cert_password)
    cert_installer.install_certificate()

    driver_setup = ChromeDriverSetup(cert_name)
    driver_setup.start_driver()
    driver_setup.import_certificate_check()

    logger.info("Script execution complete. Sleeping for 600 seconds for manual inspection...")
    time.sleep(600)
    driver_setup.close_driver()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import a certificate into Chrome.')
    parser.add_argument('-c', '--cert', type=str, help='The name of the certificate file without extension.')
    parser.add_argument('-p', '--password', type=str, help='The password for the certificate.')
    args = parser.parse_args()

    main(args.cert, args.password)
