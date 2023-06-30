import re
import urllib.parse
import webbrowser
import PySimpleGUI as sg


def main():
    # Specify theme
    sg.theme('SystemDefaultForReal')

    # List of exams available
    # TODO: Find someway to optimize this atrocious way of aligning checkboxes
    exams = [
        {'key': 'ip', 'name': 'ITパスポート                    ', 'url': 'https://itpassportsiken.com/kakomon'},
        {'key': 'sg', 'name': '情報セキュリティマネジメント試験', 'url': 'https://sg-siken.com/kakomon'},
        {'key': 'fe', 'name': '基本情報技術者試験              ', 'url': 'https://fe-siken.com/kakomon'},
        {'key': 'ap', 'name': '応用情報技術者試験              ', 'url': 'https://ap-siken.com/kakomon'},
        {'key': 'sc', 'name': '情報処理安全確保支援士試験      ', 'url': 'https://sc-siken.com/kakomon'}
    ]

    # Show checkboxes for each exam
    column_size = 2
    column_font = ('MS Gothic', 9)

    exam_checkboxes = []
    for s in range(0, len(exams), column_size):
        checkbox_slice = exams[s:s + column_size]
        row = []
        for exam in checkbox_slice:
            row.append(sg.Checkbox(exam['name'], key=exam['key'], font=column_font))
        exam_checkboxes.append(row)

    # Set window layout
    layout = [
        # Show input box
        [sg.Input(key='word', size=(0, 0), expand_x=True)],
        # Show checkboxes for each exam
        [sg.Frame('', exam_checkboxes)],
        # Show 'GO' and 'PIN' button
        [sg.Button('GO', button_color='white on green', size=(20, 1), key='go'), sg.Checkbox('📌', enable_events=True, key='pin', font=('Segoe UI Emoji', 10))]
    ]

    # Instance of GUI with hardcoded icon
    icon_base64 = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAAxnpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDsMgDPvPKXYEiFMex6FrJ+0GO/4MpFU7zRImiSMTIvvn/ZJHh0YTW3JJNaVAWLWqjUEJE21wDDZ4wFxifqvLKShL4I2ZluT9Rz2eBvNqjJaLUXm6sN6F6i9o+THyh9AnUgabG1U3gk4hukGb3wqplnz9wrqHO8o80gl5eJ8mv7llbm9bWITqjohABmwOgH4gaAwSWZHZ2IsNhkyOSD4JF/JvTwfkC+RYWR9wjj+tAAABhWlDQ1BJQ0MgcHJvZmlsZQAAeJx9kT1Iw0AcxV9btSIVETtIcchQnayDFnEsVSyChdJWaNXB5NIvaNKQpLg4Cq4FBz8Wqw4uzro6uAqC4AeIq4uToouU+L+k0CLGg+N+vLv3uHsHeJtVphg9MUBRTT2diAu5/Krgf0UfQhjGFKIiM7RkZjEL1/F1Dw9f7yI8y/3cn2NQLhgM8AjEMabpJvEG8eymqXHeJw6ysigTnxNP6nRB4keuSw6/cS7Z7OWZQT2bnicOEgulLpa6mJV1hThKHJYVlfK9OYdlzluclWqdte/JXxgoqCsZrtMcQwJLSCIFARLqqKAKExFaVVIMpGk/7uIP2f4UuSRyVcDIsYAaFIi2H/wPfndrFGemnaRAHOh9sayPccC/C7QalvV9bFmtE8D3DFypHX+tCcx9kt7oaOEjYGgbuLjuaNIecLkDjD5poi7ako+mt1gE3s/om/LAyC0wsOb01t7H6QOQpa6Wb4CDQ2CiRNnrLu/u7+7t3zPt/n4AKndy8OqJhgwAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjQzNGYzNmNkLTJjM2EtNGQ2MS1hNjlhLTAwNWM5NGEzMjZiNyIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpmNTg5ZmYyYy1mOGY2LTQ2YTMtOThhZC04NWUxN2Q3YWNkMTkiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo5ZTVkMGY5Mi1lMjIzLTQ3OGItODllOC05NjMyZDQwZWE5MTUiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTY4NzgwMTYzNjc4OTI2MSIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjM0IgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMzowNjoyN1QwMjo0NzoxNiswOTowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjM6MDY6MjdUMDI6NDc6MTYrMDk6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDowMmU0MzU4MS01NWFjLTRhOWMtYWU3YS1mMTBhZjA2YjJiOTIiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjMtMDYtMjdUMDI6NDc6MTYiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+Nw95jAAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+cGGhEvEGU+Io8AAAuySURBVGje7Rp7TFPX+94KFGpLqQVxTsFhHI/UipkaY6Ak6HSWiSHxsYlKDJopLmzM+NgjwshW3aZLwMdUxI0tAVkMTLeB0ohaBYLKQiHB8ralrHDtAywtvb3c298fZzm79nFpKbgt+X1/3X79znfOd77vfK9zUIfDgfyXgYX8x8EHAcbHxw0GA0VR/0kBdDpdZmamSCSqrKz8d1mdwzsoLy8H9HFxcUaj0fGvAW81oNfrwcfQ0JDdbmfekaamptLS0u7u7peggACn3yaTCcOwZ8+eWSyWwcFBHMcB/rfffgMfc+fO5XA4DBy7uro2bNhgNptFIlFtbe2CBQtekgnZ7faysrLFixejKMpAHx4eXlxc3NvbS1GUW50+evQIEn/33XfMBkBRFEmSJEl64jYpoPBEKhSK1NRUkiS9EVsoFO7fv3/Tpk1Lly51UojFYpFK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'
    window = sg.Window('過去問検索くん', layout, icon=icon_base64, finalize=True)
    window['word'].bind('<Return>', '_Enter')

    # Event loop
    while True:
        # Wait for the event
        event, values = window.read()
        # Exit the program when top-right X button is pressed
        if event == sg.WIN_CLOSED:
            break

        # Toggle always on top
        if event == 'pin':
            window.TKroot.wm_attributes('-topmost', values['pin'])

        # Start the search when 'GO' button is pressed
        elif event == 'go' or 'input' + '_Enter':
            # Only start searching when the search text is there and at least one exam is selected
            del values['pin']
            if values['word'] and True in values.values():
                # Enclose values other than 'AND' and 'OR' with double quotation marks
                words = re.split('\\s+', values['word'])
                words = [f'"{word}"' if word not in ['AND', '&', 'OR', '|'] else word for word in words]
                query = ' '.join(words) + ' ' + ' OR '.join('site:' + e['url'] for e in exams if values[e['key']] is True)

                # Encode the search query and open up default browser
                query = urllib.parse.quote(query)
                url = 'https://www.google.com/search?q=' + query
                webbrowser.open(url)


if __name__ == '__main__':
    main()
