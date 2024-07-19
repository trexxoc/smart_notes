#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, \
    QHBoxLayout, QRadioButton, QMessageBox, QTextEdit, QListWidget, QLineEdit, QInputDialog, QMessageBox
import json




TEXT = 'текст'
TAGS = 'тэги'
FILENAME ='notes.json'
SEARCH_TXT = 'Искать заметки по тегу'
IN_PROGRESS_TXT = 'Сбросить поиск'


NOTES = {
	"Note Name": {
		TEXT: 'Some text',
		TAGS: ['tag1', 'teg2']
	},
	"О змеях": {
		TEXT: 'Тайпаны - род очень ядовитых змей',
		TAGS: ['Тайпаны', 'факт']
	},
}





def white_notes(notes):
    with open(FILENAME, 'w') as file:
        json.dump(notes, file)





def read_notes():
    with open(FILENAME, 'r') as file:
        notes = json.load(file)
        return notes



def filter_dict(my_dict, value):
    filtered_dict = {} 
    for item in my_dict:
        if value in my_dict[item][TAGS]:
            filtered_dict[item] = my_dict[item] 
    return filtered_dict



def errorWindow(txt, title='Ошибка!'):
    msg_window = QMessageBox()
    msg_window.setWindowTitle(title)
    msg_window.setText(txt)
    msg_window.exec()






def show_notes():
    note_name = spisok.selectedItems()[0].text()
    notes = read_notes()
    txt = notes[note_name][TEXT]
    entry_field.setText(txt)
    tags = notes[note_name][TAGS]
    spisok_tag.clear()
    spisok_tag.addItems(tags)
    




def add_notes():
    text, ok = QInputDialog.getText(main_window, 'Добавить заметк', 'Введите название заметки')
    if ok:
        NOTES[text] = { TEXT: '', TAGS: [] }
        spisok.clear()
        spisok_tag.clear()
        spisok.addItems(NOTES)
        spisok_tag.addItems(NOTES[text][TAGS])
        white_notes(NOTES)





def delete_notes():
    if spisok.selectedItems():
        note_name = spisok.selectedItems()[0].text()
        del NOTES[note_name]
        spisok.clear()
        spisok_tag.clear()
        spisok.addItems(NOTES)
        white_notes(NOTES)
    else:
        errorWindow('заметка не выбрана!')







def save_notes():
    if spisok.selectedItems():
        note_name = spisok.selectedItems()[0].text()
        note_text = entry_field.toPlainText()
        NOTES[note_name][TEXT] = note_text
        white_notes(NOTES)
    else:
        errorWindow('заметка не выбрана!')




def search_by_tag():
    text2 = teg.text()
    if button_search.text() == SEARCH_TXT and text2 != '':
        button_search.setText(IN_PROGRESS_TXT)
        filtered_notes = filter_dict(NOTES, text2)
        spisok.clear()
        spisok_tag.clear()
        entry_field.clear()
        spisok.addItems(filtered_notes)
    elif button_search.text() == IN_PROGRESS_TXT:
        button_search.setText(SEARCH_TXT)
        spisok.clear()
        spisok_tag.clear()
        entry_field.clear()
        spisok.addItems(NOTES)






def add_tag():
    if spisok.selectedItems():
        note_name = spisok.selectedItems()[0].text()
        text2, ok = QInputDialog.getText(main_window, 'Добавить тег', 'Введите теги через пробел')
        if ok:
            NOTES[note_name][TAGS] += text2.split(' ')
            spisok_tag.clear()
            spisok_tag.addItems(NOTES[note_name][TAGS])       
            white_notes(NOTES)
    else:
        errorWindow('заметка не выбрана!')



def delete_tag():
    if spisok.selectedItems():
        if spisok_tag.selectedItems():
            note_name = spisok.selectedItems()[0].text()
            tag_name = spisok_tag.selectedItems()[0].text()
            NOTES[note_name][TAGS].remove(tag_name)
            spisok_tag.clear()
            spisok_tag.addItems(NOTES[note_name][TAGS])
            white_notes(NOTES)
        else:
            errorWindow('тэг не выбрана!')
    else:
        errorWindow('заметка не выбрана!')



#white_notes(NOTES)
NOTES = read_notes()


app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('Умные заметки')

entry_field = QTextEdit()

spisok = QListWidget()
spisok.addItems(NOTES)
spisok.itemClicked.connect(show_notes)


spisok_tag = QListWidget()

teg = QLineEdit()

button_create = QPushButton('Создать заметку')
button_create.clicked.connect(add_notes)

button_delete = QPushButton('Удалить заметку')
button_delete.clicked.connect(delete_notes)

button_save = QPushButton('Сохранить заметку')
button_save.clicked.connect(save_notes)

button_add = QPushButton('Добавить к заметке')
button_add.clicked.connect(add_tag)

button_unpin = QPushButton('Открепить от заметки')
button_unpin.clicked.connect(delete_tag)

button_search = QPushButton(SEARCH_TXT)
button_search.clicked.connect(search_by_tag)

text = QLabel('Список заметок')
text2 = QLabel('Список тегов')

hbox = QHBoxLayout()
hbox.addWidget(button_create)
hbox.addWidget(button_delete)

hbox2 = QHBoxLayout()
hbox2.addWidget(button_add)
hbox2.addWidget(button_unpin)


vbox = QVBoxLayout()
vbox.addWidget(text)
vbox.addWidget(spisok)
vbox.addLayout(hbox)
vbox.addWidget(button_save)
vbox.addWidget(text2)
vbox.addWidget(spisok_tag)
vbox.addWidget(teg)
vbox.addLayout(hbox2)
vbox.addWidget(button_search)


main_layout = QHBoxLayout()
main_layout.addWidget(entry_field)
main_layout.addLayout(vbox)

main_window.setLayout(main_layout)








main_window.show()

app.exec_()




