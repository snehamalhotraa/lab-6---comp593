import os
import hashlib
import requests

def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)
    else:
        print("The downloaded installer is corrupted or tampered with.")

def get_expected_sha256():
    """Downloads the text file containing the expected SHA-256 value for the VLC installer file from the 
    videolan.org website and extracts the expected SHA-256 value from it.

    Returns:
        str: Expected SHA-256 hash value of VLC installer
    """
    url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    response = requests.get(url)
    if response.ok:
        # Extract the SHA-256 hash from the response content
        content = response.text
        # Assuming the format is: SHA-256_HASH  FILENAME
        expected_sha256 = content.split()[0]
        print(f"{expected_sha256} matched")
        return expected_sha256
    else:
        raise Exception("Failed to download the SHA-256 checksum file")

def download_installer():
    """Downloads, but does not save, the .exe VLC installer file for 64-bit Windows.

    Returns:
        bytes: VLC installer file binary data
    """
    url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    response = requests.get(url)
    if response.ok:
        return response.content
    else:
        raise Exception("Failed to download the VLC installer")

def installer_ok(installer_data, expected_sha256):
    """Verifies the integrity of the downloaded VLC installer file by calculating its SHA-256 hash value 
    and comparing it against the expected SHA-256 hash value. 

    Args:
        installer_data (bytes): VLC installer file binary data
        expected_sha256 (str): Expected SHA-256 of the VLC installer

    Returns:
        bool: True if SHA-256 of VLC installer matches expected SHA-256. False if not.
    """    
    image_hash = hashlib.sha256(installer_data).hexdigest()
    print(image_hash)
    return image_hash == expected_sha256
    

def save_installer(installer_data):
    """Saves the VLC installer to a local directory.

    Args:
        installer_data (bytes): VLC installer file binary data

    Returns:
        str: Full path of the saved VLC installer file
    """
    installer_path = os.path.join(os.getcwd(), 'vlc_installer.exe')
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
    return installer_path

def run_installer(installer_path):
    """Silently runs the VLC installer.

    Args:
        installer_path (str): Full path of the VLC installer file
    """    
    os.system(f'start /wait {installer_path} /S')

def delete_installer(installer_path):
    """Deletes the VLC installer file.

    Args:
        installer_path (str): Full path of the VLC installer file
    """
    if os.path.exists(installer_path):
        os.remove(installer_path)

if __name__ == '__main__':
    main()