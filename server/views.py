from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import os
import xml.etree.ElementTree as ET
import json
import re
import operator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FileUploadForm(forms.Form):
    file = forms.FileField(label = "File upload")

def handle_uploaded_file(f):
    save_path = os.path.join(BASE_DIR + '/files', f.name)
    with open(save_path, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)

def index(request):
    import nltk
    '''
    msg : messsage of uploading
    data : for outputing(include article, context, number of characters, words, and phrases)
    file : save file's name
    user_search : user's search 
    search_err : saveing message when search error occur
    new_title : title temp
    delete_msg : delete message
    num_words,num_phrases,num_ch,num_search: caculate number of characters, words, and phrases
    '''
    msg = data = file  = user_search  = search_err = new_title = delete_msg = ""
    num_words = num_phrases = num_ch = num_search = 0
    words = phrases = ch = []
    if request.method == 'POST':
        forms = FileUploadForm(request.POST,request.FILES)
        if forms.is_valid():
            file_name = str(request.FILES['file'])
            if file_name.endswith('.xml') != True and file_name.endswith('.json') != True:
                msg = 'Format error ( .xml or .json) : ' + file_name
                return render(request,'index.html', locals())
            handle_uploaded_file(request.FILES['file'])
            msg = '"' + file_name + '"' + ' upload successfully! '
            files = os.listdir(BASE_DIR + '/files')
        else: 
            if "ok" in request.POST:
                if 'file_name' not in request.GET:
                    search_err = 'There is no file you can search!'
                else:
                    if request.POST['search'] == '':
                        search_err = 'Your input is empty!'
                    else:
                        user_search = request.POST['search']
            elif "delete" in request.POST:
                delete_path = os.path.join(BASE_DIR + '/files', str(request.POST['delete']))
                os.remove(delete_path)
                delete_msg = "File is deleted successfully."
            else:
                msg = 'The submitted file is invalid ( empty... ).'
            forms = FileUploadForm()
    else:
        forms = FileUploadForm()
    files = os.listdir(BASE_DIR + '/files')

    if 'file_name' in request.GET:
        xmlfile = jsonfile = ''
        file = request.GET['file_name']
        data = []
        if file.endswith('.xml') == True:
            tree = ET.parse('files/' + file)
            root= tree.getroot()
            if user_search == "" or user_search == " ": #no search, just output the file and static
                for titles in root.findall(".//Article"):
                    title = titles.find(".//ArticleTitle") #get the title 
                    new_title = title.text
                    the_search = 0
                    if user_search != "":
                        the_search += title.text.count(user_search)
                        new_title = title.text.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search))
                    text = []
                    the_char = 0
                    the_words = 0
                    the_phrases = 0
                    for context in titles.findall(".//AbstractText"): #get the abstracts
                        for i in context.text:
                            if ord(i) < 127 and ord(i) >= 33:
                                the_char += 1
                        phrases = nltk.sent_tokenize(context.text) 
                        sentences = []
                        label = str(context.get('Label'))
                        if user_search != "":
                            for sentence in phrases:
                                the_search += sentence.count(user_search)
                                sentences.append(sentence.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search)))
                            phrases = sentences
                            if label != "None":
                                the_search += label.count(user_search)
                                label = label.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search))
                                text += [['[' + label + ']', phrases]] #get the labels and phrases in the abstract
                            else:
                                text += [['', phrases]] 
                        else:
                            if label != "None": 
                                text += [['[' + label + ']', phrases]] #get the labels and phrases in the abstract
                            else:
                                text += [['', phrases]] 
                        words = context.text.split( )
                        num_words += len(words)
                        the_words += len(words)
                        num_phrases += len(phrases)
                        the_phrases += len(phrases)
                    num_ch += the_char
                    num_search += the_search
                    if user_search == "":
                        data += [[new_title, text, the_char, the_words, the_phrases]]
                    else:
                        data += [[new_title, text, the_char, the_words, the_phrases, the_search]]

            else:   
                for titles in root.findall(".//Article"):
                    title = titles.find(".//ArticleTitle")
                    new_title = ""
                    the_search = 0
                    for word_in_titles in title.text.split():
                        if operator.contains(word_in_titles, user_search):
                            the_search += word_in_titles.count(user_search)
                            new_title += word_in_titles.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search)) + ' '
                        else:
                            new_title += word_in_titles + ' '
                    text = []
                    the_char = 0
                    the_words = 0
                    the_phrases = 0
                    for context in titles.findall(".//AbstractText"):
                        for i in context.text:
                            if ord(i) < 127 and ord(i) >= 33:
                                the_char += 1
                        phrases = nltk.sent_tokenize(context.text)
                        sentences = []
                        for sentence in phrases:
                            new_sentence = ""
                            for word in sentence.split( ):
                                if operator.contains(word, user_search):
                                    the_search += word.count(user_search)
                                    new_sentence += word.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search)) + ' '
                                else:
                                    new_sentence += word + ' '
                            sentences.append(new_sentence)

                        new_label = ""
                        if str(context.get('Label')) != "None":
                            label = '[' + str(context.get('Label')) + ']'
                            for word_in_label in label.split():
                                if operator.contains(word_in_label, user_search):
                                    the_search += word_in_label.count(user_search)
                                    new_label += word_in_label.replace(user_search, '<span class="bg-warning ">{}</span>'.format(user_search)) + ' '
                                else:
                                    new_label += word_in_label + ' '
                        text += [[new_label, sentences]]
                        words = context.text.split( )
                        num_words += len(words)
                        the_words += len(words)
                        num_phrases += len(phrases)
                        the_phrases += len(phrases)
                    num_ch += the_char
                    num_search += the_search
                    data += [[new_title, text, the_char, the_words, the_phrases, the_search]]
                    
            xmlfile = file
        elif file.endswith('.json') == True:
            with open(os.path.join('files/', file), encoding="utf-8") as json_file:
                datas = json.load(json_file)
                if user_search == "" or user_search == " ":
                    for user in datas:
                        new_user = user['username']
                        the_search = 0
                        if user_search != "":
                            the_search += new_user.count(user_search)
                            new_user = new_user.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search))
                        text = user['tweet_text']
                        the_char = 0
                        the_words = 0
                        the_phrases = 0
                        for i in text:
                            if ord(i) < 127 and ord(i) >= 33:
                                the_char += 1
                        num_ch += the_char
                        phrases = nltk.sent_tokenize(text)
                        num_phrases += len(phrases)
                        the_phrases += len(phrases)
                        words = text.split( )
                        num_words += len(words)
                        the_words += len(words)
                        text = text.split('\n')
                        if user_search != "":
                            sentences = []
                            for sentence in text:
                                the_search += sentence.count(user_search)
                                sentences.append(sentence.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search)))
                            text = sentences
                        num_search += the_search
                        if user_search == "":
                            data += [[new_user, text, the_char, the_words, the_phrases]]
                        else:
                            data += [[new_user, text, the_char, the_words, the_phrases, the_search]]

                else:
                    for user in datas:
                        new_user = ""
                        the_search = 0
                        if operator.contains(user['username'], user_search):
                            the_search += user['username'].count(user_search)
                            new_user += user['username'].replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search)) + ' '
                        else:
                            new_user += user['username'] + ' '
                        text = user['tweet_text']
                        the_char = 0
                        the_words = 0
                        the_phrases = 0
                        for i in text:
                            if ord(i) < 127 and ord(i) >= 33:
                                the_char += 1
                        num_ch += the_char
                        phrases = nltk.sent_tokenize(text)
                        
                        text_split = text.split('\n')
                        sentences = []
                        for words in text_split:
                            new_sentence = ""
                            for word in words.split( ):
                                if operator.contains(word, user_search):
                                    the_search += word.count(user_search)
                                    new_sentence += word.replace(user_search, '<span class="bg-warning">{}</span>'.format(user_search)) + ' '
                                else:
                                    new_sentence += word + ' '
                            sentences.append(new_sentence)
                        num_phrases += len(phrases)
                        the_phrases += len(phrases)
                        words = text.split( )
                        num_words += len(words)
                        the_words += len(words)
                        text = text.split('\n')
                        num_search += the_search
                        data += [[new_user, sentences, the_char, the_words, the_phrases, the_search]]
            jsonfile = file
    return render(request,'index.html', locals())