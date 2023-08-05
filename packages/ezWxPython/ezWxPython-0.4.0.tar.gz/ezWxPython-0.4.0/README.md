
# ezWxPython

ezWxPython is inspired by the pySimpleGUI project and is a wrapper project that makes it easy to create a wxPython Application. It is built on an event driven approach while pySimpleGUI is based on message driven.

Since the ordered dict used in menubar generation is supported from python 3.6, you have to use with phtyon 3.6+ if you want to use menubar.

## Example Application

Full source : /demo/BasicForm.py 

```python
import ezWxPython as ezwx
   
######################################################################
# Layout
######################################################################
        
exit_png='eJwBZgWZ+olQTkcNChoKAAAADUlIRFIAAAAgAAAAIAgGAAAAc3p69AAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAUISURBVHjavFfdaxxVFP/de/cj28221hpBTIlNX6qQ9EUNQg1RKKYsfRBfFIL2oeC70AdBfPBJqIr/QLHEKMWH+hFrsxQCarVfVNFEDNU0pGlTTGJTapO4M3Pv9Zw7dze7ss3OImaTk8nOzL3nN7/zOx8DbO5HTF/4srg690P0wZF+S98zqc1yfKn04a5HdnZ+KmF6RSoNJSSfz8tNcK7mfyp9sru7a3pt6bfeubPHYKIIQgi+lm7GQOqjNwY/y2VkUdICkdCjsRZBEKC7Zx+6HnsK4eot3Jj4DtHqMkDXjDVQKn72ZgBy2ZQovnVqjYJFABIiMMZi5e8Alw/tw7Wfx3F3aRZCkisya0JYTQzIZADaRIwCbXRnKwCsTeP69yNYKxtax27IIT05/cIQAOU3awZACCvA9DNgmRAAB0spBUuLjOCQwFEPG4dH67CiASTIAgtJ8WoFAH/4fnZGzxwDAHz86XwUuj0TARBGgu+V0iYHQPcRAUQ3h8K6h68AsJ6BSggapWHm4Huwzx3FSQYoNYdAEWWyZdMEwGjrNFFnTUSY1ySU/l14/q83sSLKyqFVxEBSEXKsJdFlbQMG6EeHodPVvRhIBxp4oe91PNuLobHCOSibpQUp2lS2YMrlu9OBN81HzgIqRKqGgXTxHSyGGtvcRUK7VqYjchjsfREldQK/L38DOzkAmQkJsk4iAacZ7fczLgEEOSdWSFORC8F6FuTZ+fFXj+FW+XOunLSQbrD3Y2L+BA70vgyZHsZ5+TXUL8/QxgHtbhKEwMYiNHEI2Hn3QzPo2DqPuWiw0gscgAw/+Z3yAr698sV6uRWj5BiY/GMYgz2HKG2O46IcR9vUAO0exV42AMBZoI1xT6+tcNQ/eN8ShkuPYqCoqwxUNbCi5ykYcCYyZHwkeJY2uvLnx3hizx5EnTfdSady2cxUjQh9LSCf+VwaJgycTqpZwFhW7Q2oLKoMWFNTUFIBLk1PITPf6WoCmD5hNy5EwhciW9GBcSxsyaYRUiHyEYgZ4E1DdRPZPMVjC5GQowuZ2FJtwOwicKHURfTvJwKotis4CpuZ9nlvybMlAAu3d+DAkz9SIYrqNMAA7h4dPtfOCFkwlCV45aU4ylevA5fHulC4uh8yG3jIsqkIlRJx57PC7UkqwNS1nTh9Po++p8t1zSg4dQT9dNzuo5EefBunmYVfp4HF8Q4Upkm1GcpNaZs7r4ZA1IXAoaLd2/OpuBn5XsB/V8hmyCbJJvh/VvDMHFA6ia8Glh6HzRrOzgTCWzcWmTE1qegtT609IhHW9gKqLrhNtuBtmQSMM6M4e/F9vKup8PB3qURrlZCewpj6SsiWSVGPoBhLee92HI6+hr3+/yiSsWJ5QeJmyIXINugFflxjBnIbNCMOySzfS1bQdHC0CosWehFpQLrarxsACHWw4TwQeHMzIS9WFANmTMAmHQcotipuxdrWrXL9hhgQqYQTEeewiz9EawxwA+IZ0P4LNjMQUh3ItzCSudLr+plNPBJxCOIuiPWRzI+GJipTWHPJAKRFRG8PirOwhfcCXhfrJpaSqILgg2OgRoSZoaGhcsONaOHYMqt6yX9LHgJtJc7MFLAjF6GzECKfMoiHY86CcnUicgPJyMjIbp4LGhHgz2f+6/vZA9tyucPFnoMPd7T3bS9gb6UbCr953jv7315O/f7tZFvJqOXhDlddgc37KP+wWQ+Gp5qVfwQYAOMRch38qZCKAAAAAElFTkSuQmCCWbl5kg=='
save_png="eJyVVH1MG2UYPyhjjJWvhOgkQY5Dp9nW3l2/e6Urd70eNK4dKSXUMEOP9kpvbe9ud1daiBFly3RmH0TjmAnJNjRRM2ec0T8WTEAxOuIfw49E58KoJJqpW0A0jmWVecUWiTEkvsm97/s87+/3fL7vHWv3tlaU15UDAFDhbiN9ygrmvrJSZZYGB39XlodkV0Du4CNyihYZAA/zvQzoTtB9jI+hwwOHZphmAFBdZP0BOeDZh4X4hJbOYbTphADkRrMjLdChGCODvUwfy9mhxYlJCGTDdqjL6EE8gpOJsm2DItMx6PWHBmMhaxhy7AWb05hiIMHINJhOxDkJS9uhNbuYss+pYQhcg8gxO/R3UAFPO+jkRQY0ahFNCDEhoAnVonqD2WzeA+oQFIERHYzqNKgZ0+swBAHzA1K8ieEI5iOpvC9FskNRWRYwGE6lUtqUXsuLfTBqtVpzNnQ6jYLQSAOcTKc1nNRUsEAyUkhkBZnlOTAn0718UrZDUCGFhOBj+6KytG6ck/LFUsoGp2kBRrUILK5h4A0sj2dzRiKxjpZkHxPZHC35BwQG9jESnxRDShcjTRtcbU7NAfM5YB5ajDFKFyk6LjFrBx4Ptl8JnuXoOMmHkgmGk92kHUom2TCGu/SUwYRYLJTFSrpQFLeYEKuVQnUorkMMOmvBwEaiotGGFa6FxC0oSZkIo4tCURdC4LieIFwG0kygeiNKFrhuTpJpLsQUuOw/XOOmXMwpMrTMi36ejxduU3uUl3kpygugs8MIdrFcmE9JuUbn42REtp8JUyKfANdqjrH/4V2vcxFWg4F0UYp/BEWtOGHAKdKK6K2U3ugioDw3/L/LBSuRwP+6cwWVcpFz2/UXpAjrb5DhlJaJygubCe63AUDRhJvE/enverP37zumW4o/xX949ugHfb/gtfW3EtEyE1eCBmYfne184O6O9nj3/Ont6sCtj34G1EtVO4jdp27svL4sxDo/XH68cuXqUsMFFXHRf6UfaHOYpEu2jCNBAD1YqwScrl7Zqi56opwA3mzo8YbwO5pIGYLsscmH41vJa2zQOHqzeuW3xQbnmRN11yqBnx7bW7JK78pur+1+OqMoXkjOfnxQu61x6Wzjl96Xh6vPIRXZLaXfZ+dGr/S3jF94+FcWiNUCxs8u33zpNjDyzPhrmYaTccuhafd79SMNQe+TZQeGsicbq6Jll4HXzx6pXnn+fCbzSmtw3+4WpCRaUfqq6l2y6Kn6pZShfJU+NTzDasPdI7ZYlS6lr763IE8tTg5dGo3UHlFr9UpSV3vGOnepw575Y5BZ81X9pGp15EfgOFhsyywOjZVCn9cIU5H4F1PDB791OITrtRVZopw6VzcmBpxV52+MButWVOjxmrmaydWss+twZ+WEqv3rewsnih/5ZtyycGd+yOLMKPMnRwF0S82LvSNNpucO/PngW5irY3pptGV+Gf7j7TnEYntDVQQUq4Hbxp13z7zPbMv9Zd0uL/kOERz+C2G1BH0="

menu_def = { 
    "File" : { 
        "Option" : { 
            "Settings" : None,        # Disabled menu item
            "Copy": onCopy 
        }, 
        "-" : None,                   # Menu separator
        "Exit" : [onExit, exit_png],  # Menu item with base64-encoded icon image
        "-2" : None,                  # Menu separator (should have different name from other menu separator) 
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

tool_def = [ #icon, text, handler
    [exit_png, onExit, "Exit" ],
    [None],                         # Tool separator
    [save_png, None, "Save", ],     # Disabled toolbar item
]

status_def = [
    ["Ready", -6],   # width will have space with proportion 6 
    ["Status", -4],  # width will have space with proportion 4
    ["Code:1", 20]   # fixed width
]

body_def = [
    [ ezwx.Label ("Folder: "), 
      ezwx.Text  ("Default Text",key="folder",expand=True,password=True,proportion=1), 
      ezwx.Button("Folder", handler=onBrowse, key="browse"),
      ezwx.Button("Files", handler=onFileBrowse, key="file_browse" ), ],
    [ ezwx.Check("Check1", handler=onCheck, key='check1'),
      ezwx.Check("Check2", key='check2'), 
      ezwx.Link("Google", "https://www.google.com"), ],
    [ ezwx.Label ("Choices: "), ezwx.Choice(['apple','orange','grape'],0,handler=onChoice,key="choice"),
      ezwx.Label ("  ComboBox: "), ezwx.Combo (['apple','orange','grape'],"orange",handler=onCombo,key="combo"),
      ezwx.Label ("  Date: "), ezwx.Date  (key='date'),
      ezwx.Label ("  Time: "), ezwx.Time  (key='time'), ],
    [ ezwx.List  (['apple','orange','grape'],2,expand=True,proportion=0,handler=onList,key="list"),
      ezwx.List  (['apple','orange','grape'],2,expand=True,proportion=0,handler=onCheckList,check=True,key="checklist"),
      ezwx.Scroll( [
          [ezwx.Radio("Group",["Item1","item2","item3"],"item2",handler=onRadio,key='radio')],
          [ezwx.Button("1")],[ezwx.Button("2")],[ezwx.Button("3")],[ezwx.Button("4")],
          [ezwx.Button("5")],[ezwx.Button("6")],[ezwx.Button("7")],[ezwx.Button("8")],
          [ezwx.Button("9")],[ezwx.Button("10")],
      ], expand=True, proportion=1),
      ezwx.Notebook([
          [
              "StyledText",
              [ ezwx.StyledText ("Default\nMulti Line\nText",expand=True,proportion=1,key="stc"),
                { 'expand' : True, 'proportion' : 1 } ],
          ],      
          [
              "Text",
              [ ezwx.Text  ("Default\nMulti Line\nText",expand=True,proportion=1,multiline=True,key="text"), 
                { 'expand' : True, 'proportion' : 1 } ],
          ],
      ], expand=True, proportion=2),  
      ezwx.List([[('Name',100,-1),('Sex',32,0),('Age',64,1)], #label, width, align
                   ["Willy","M","32"],
                   ["Jane","F","28"],
          ], expand=True, proportion=2, multicol=True),
      ezwx.List(expand=False,proportion=1,label="Editable List", edit=True,key='editlist'),
      { 'proportion' : 1 }
    ],
    [ ezwx.Panel([
        [ ezwx.Button("A"), ezwx.Button("B")], 
        [ ezwx.Ticker("This is a ticker example text", expand=True, proportion=1, key='ticker')],
        [ ezwx.Line(expand=True, proportion=1)],
        [ ezwx.Slider(value=20,expand=True, proportion=1, key='slider')],
        [ ezwx.Spin(value=20,expand=True, proportion=1, key='spin')],
      ]),
      ezwx.Spliter([
          200, #sashpos
          [ 
              [ ezwx.Bitmap(filename="D:\\Lenna.png",expand=True,proportion=1,key="bitmap")],
          ],   #panel1
          240,
          [
              [ ezwx.Calendar(key='calendar',expand=True,proportion=1)],
          ],   #panel2
          160,
          [
              [ ezwx.Tree( [ 'Root', 
                             ['Item-1', [ 'Item-1.1', 'Item-1.2' ],
                              'Item-2', 
                              'Item-3', [ 'Item-3.1', 'Item-3.2', 'Item-3.3' ],
                             ] 
                          ] ,expand=True,proportion=1,key="tree"), 
                { 'expand' : True, 'proportion' : 1 } ],
          ],   #panel2
      ], expand=True, proportion=1, style='vertical'),
      { 'expand' : True, 'proportion' : 1 }
    ],
    [ None,    #Insert Spacer with proportion 1 
      ezwx.Button("ImageView", handler=onImageViewButton),
      ezwx.Button("Calendar", handler=onCalendarButton),
      ezwx.Button("Date", handler=onDateButton),
      ezwx.Button("Time", handler=onTimeButton),
      ezwx.Button("StartThread", handler=onThreadButton),
      ezwx.Button("StartTimer", handler=onTimerButton, key="button") ],
]

layout = {
    "menu"   : menu_def, 
    "tool"   : tool_def, 
    "status" : status_def, 
    "body"   : body_def, 
}

######################################################################
# Main
######################################################################

def threadTarget():
    ezwx.runAfter(onThread)

if __name__ == "__main__":
    window = ezwx.WxApp(u"ezwxApp", 900, 620)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    window.idleHandle(onIdle)
    window.timerHandle(onTimer, key='timer')
    window.run()
```

Generated Form.

![basic_form](https://3.bp.blogspot.com/-Ql19xAnsDzE/XIJusJqjHjI/AAAAAAAAAio/YMPtZcLIyD8dQql5VI0KEHVz99PmTPFsgCLcBGAs/s1600/win9.png)   


## Status

### Implemented features.

* Menubar generation from dict with text menu items + optional icon.
* Toolbar generation from list with icon buttons + optional text.
* Statusbar generation from list
* Body (Client Area) generation from 2-dimentional list. (single VBox + multiple HBoxes)
* Open Event Handler : initializing controls dynamically.
* Close Event Handler : to save data before exit.
* Idle Event Handler
* Timer Event Handler
* Thread interface : callLater(), WxAppClose()
* TextArea with Drag and Drop files
* Support Popup window which can be created same way as main window.
* Fixed size and dynamic size support for controls.

### Implemented Controls

* Bitmap : wx.StaticBitmap
* Button : wx.Button
* Calendar : wx.CalendarCtrl
* Check : wx.CheckBox
* Choice : wx.ChoiceBox
* Combo : wx.ComboBox
* Date : wx.DatePickerCtrl
* Label : wx.StaticText
* Line : wx.StaticLine
* Link : wx.adv.HyperlinkCtrl
* List : wx.ListBox, wx.CheckListBox, wx.ListCtrl, wx.adv.EditableListBox
* Progress : wx.lib.progressindicator.ProgressIndicator
* Radio : wx.RadioBox
* Spin : wx.SpinCtrl
* StyledText : wx.StyledTextCtrl
* Text : wx.TextArea + drag and drop files
* Ticker : wx.lib.tivker.Ticker
* Time : wx.TimePickerCtrl
* Tree : wx.TreeCtrl
* Web : wx.lib.iewin.IEHtmlWindow

### Implemented Containers

* Book : wx.Notebook, wx.Choicebook, wx.Simplebook
* Panel : wx.Panel
* Splitter : wx.SplitterWindow, wx.lib.splitter.MultiSplitterWindow
* Scroll : wx.ScrolledWindow

### Implemented Dialogs

* Directory Choose Dialog
* Open File Dialog with multiple file selection support (return full path)
* Save File Dialog (return full path)
* MessageBox 
* MessageYesNo : True, False
* MessageYesNoCancel : True, False, None
* ProgressDialog
* Custom Popup Window : WxPopup 

## Todo

* Tooltip support
* ContextMenu support
* More controls support
* More Containers and Sizers support
* Command shell interface
* Network interface support : ssh, sftp, ftp, telnet and etc
* 3rd party library support : matplotlib, PIL, FPDF and etc.