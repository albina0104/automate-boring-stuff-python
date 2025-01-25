# Converting Spreadsheets to Other Formats

import ezsheets

def convert_spreadsheet_to_other_formats(spreadsheet_name):
    ss = ezsheets.upload(spreadsheet_name)
    ss.downloadAsExcel()
    ss.downloadAsODS()
    ss.downloadAsPDF()
    ss.downloadAsTSV()
    ss.downloadAsHTML()
    ss.downloadAsCSV()
    print('Downloading done for all formats')


if __name__ == '__main__':
    spreadsheet_name = 'example_converting.csv'
    convert_spreadsheet_to_other_formats(spreadsheet_name)
