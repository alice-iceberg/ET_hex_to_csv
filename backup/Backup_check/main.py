import hex_to_utf
import issues_check
import tools


def main():
    # unzipping directory
    zip_hex_path_list = tools.get_today_zip_hex_path()
    for zip_hex_path in zip_hex_path_list:
        tools.unzip_hex_dir(zip_hex_path, tools.BACKUP_HEX_PATH)

    # checking backup
    directory = tools.get_today_hex_path()
    issues_check.issues_check_pipeline(directory)

    # converting to utf
    hex_to_utf.parallel_hex_to_csv(directory)


if __name__ == '__main__':
    main()
