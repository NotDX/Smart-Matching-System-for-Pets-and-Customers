from fuzzywuzzy import fuzz
import pandas as pd
import re
import jieba
import tkinter
import tkinter.messagebox
from tkinter import*

'''定义添加字典函数'''
def addword(x):
    fl = x.split('，')
    for j in range(len(fl)):
        jieba.add_word(fl[j])

def cut(df):
    x = 0
    y = 0
    flagnum = ""
    for i in range(df.shape[0]):
        flag = df.iloc[i, 0]
        flagnum = str(flagnum) + '，' + flag
    for i in range(df.shape[0]):
        flag = df.iloc[i, 0]
        result = df.iloc[i, 1]
        if result in flagnum:
            df1.loc[x] = [flag, result]
            x = x + 1
        else:
            df2.loc[y] = [flag, result]
            y = y + 1
    return df1, df2

'''类别规则库识别'''
def identify(df1, df2):
        starttemp=entry1.get()
        temp = starttemp
        temp1 = re.sub(r'[色, 物, 有, 子, 会]', "", temp)
        for i in range(df1.shape[0]):
            flag = df1.iloc[i, 0]
            addword(flag)
            result = df1.iloc[i, 1]
            addword(result)
            temp0 = jieba.lcut(temp1)
            for j in range(len(temp0)):
                if temp0[j] in re.sub('，', "", flag) and re.sub('，', "", result) not in temp:
                    temp = temp + '，' + re.sub('，', "", result)
                    text.insert(END, "类别库规则r" + str(i) + "：IF " + flag + " THEN 为" + result + "匹配成功，\n更新事实为：" + temp + '\n\n')
        if temp == starttemp:
            text.insert(END, "未在类别库中找到这些特征，继续识别的结果可能不准确。\n")
        '''名称规则库识别'''
        while(len(temp.split('，')) < 4):
            #te = input("特征过少，请继续添加特征...\n")
            text.insert(END, "特征过少，请继续添加特征...\n")
            te = entry1.get()
            if te in temp:
                text.insert(END, "特征重复，请重新输入...\n")
            else:
                temp = temp + '，' + te
        temp1 = re.sub(r'[色, 物, 有, 子, 会]', "", temp)
        temp0 = jieba.lcut(temp1)
        n = 0
        num = 0
        for i in range(df2.shape[0]):
            flag = df2.iloc[i, 0]
            addword(flag)
            result = df2.iloc[i, 1]
            addword(result)
            m = 0
            for j in range(len(temp0)):
                m = m + fuzz.partial_ratio(temp0[j], re.sub('，', "", flag))
            if num < m:
                num = m
                n = i
        flag0 = df2.iloc[n, 0]
        result0 = df2.iloc[n, 1]
        if num == 0:
            text.insert(END, "抱歉，识别失败，请等待后续规则库完善...\n")
        else:
            text.insert(END, "名称库规则r" + str(n) + '：IF ' + flag0 + " THEN 为" + result0 + "匹配成功!\n")
            if num < 600:
                text.insert(END, "结果可能为：" + result0 +'\n')
            else:
                text.insert(END, "推出结果为：" + result0 +'\n')

'''定义规则输出模块'''
def rule(df1, df2):
    #starttemp = input("请输入要输出特征的结果：\n")
    starttemp = entry1.get()
    temp = starttemp
    for i in range(df2.shape[0]):
        flag = df2.iloc[i, 0]
        result = df2.iloc[i, 1]
        if starttemp in result or result in starttemp:
            text.insert(END, "名称库规则r" + str(i) + "：IF " + flag + " THEN 为" + result + "匹配成功，\
                  \n得到结果" + starttemp + "的特征为：" + flag + "\n")
            temp = starttemp + '，' + flag
    for i in range(df1.shape[0]):
        flag = df1.iloc[i, 0]
        result = df1.iloc[i, 1]
        if temp in result or result in temp:
            text.insert(END, "类别库规则r" + str(i) + "：IF " + flag + " THEN 为" + result + "匹配成功，\
                  \n得到结果" + starttemp + "的特征为：" + flag + "\n")
            temp = temp + '，' + flag
    if temp == starttemp:
        text.insert(END, "该结果在规则库中匹配失败，请等待后续规则库完善...\n")

'''定义规则增加模块'''
def insert(df, excelFile):
    f = 1
    while (f == 1):
        flag0 = entry1.get()
        result0 = entry2.get()
        resultnum = ""
        flagnum = ""
        for i in range(df.shape[0]):
            flag = df.iloc[i, 0]
            flagnum = flagnum + '，' + flag
            result = df.iloc[i, 1]
            resultnum = resultnum + '，' + result
        if result0 in resultnum:
            text.insert(END, "当前结果已在规则库中存在，请重新添加或选择修改该结果的特征...\n")
            break
        else:
            df.loc[len(df)] = [flag0, result0]
            text.insert(END, "该规则添加成功！\n")
            break
    df.to_excel(excelFile, sheet_name='df', index=False)

'''定义规则修改模块'''
def update(df, excelFile):
    f = 1
    while (f == 1):
        f1 = 0
        result0 = entry1.get()
        for i in range(df.shape[0]):
            flag = df.iloc[i, 0]
            result = df.iloc[i, 1]
            if result0 == result:
                #print("当前规则为：IF " + flag + " THEN " + result)
                text.insert(END, "当前规则为：IF " + flag + " THEN " + result + "\n")
                flag = entry2.get()
                df.loc[i] = [flag, result]
                f1 = 1
                #print("该规则修改成功，", end='')
                text.insert(END, "该规则修改成功！\n")
                break
        if f1 == 0:
            text.insert(END, "该规则不存在！\n")
            #print("该规则不存在", end='，')
        break
    df.to_excel(excelFile, sheet_name='df', index=False)


'''定义规则删除模块'''
def delete(df, excelFile):
    f = 1
    while (f == 1):
        f1 = 0
        result0 = entry1.get()
        for i in range(df.shape[0]):
            result = df.iloc[i, 1]
            if result0 == result:
                df = df.drop([i])
                f1 = 1
                #print("", end='')
                text.insert(END, "该规则删除成功！\n")
                break
        if f1 == 0:
            text.insert(END, "该规则不存在！\n")
        break
    df.to_excel(excelFile, sheet_name='df', index=False)

'''得到初始规则库'''
excelFile = r'rule2.xlsx'
df = pd.DataFrame(pd.read_excel(excelFile, sheet_name = 'df'))
df1 = pd.DataFrame(columns = ["flag", "result"])
df2 = pd.DataFrame(columns = ["flag", "result"])
[df1, df2] = [cut(df)[0], cut(df)[1]]


#GUI
#clear
def clear():
    entry1.delete(0, END)
    entry2.delete(0, END)

#退出专家系统
def wayout():
    b=tkinter.messagebox.askyesno('注意','您即将退出系统')
    if b:
        sys.exit(0)


# 创建登入窗口
win = tkinter.Tk()
win.geometry('800x700')
win.title("宠物推荐及查询系统")

# 创建登入界面
msg = "❤欢迎使用宠物推荐及查询系统❤"
#sseGif = PhotoImage(file="cutie.gif")
logo = Label(win, text=msg,  font=("Courier", 20, "bold"), compound=BOTTOM)
#logo = Label(win, image=sseGif, text=msg,  font=("Courier", 20, "bold"), compound=BOTTOM)
logo.pack(pady=10)

#文本框
instruction1 = "宠物推荐：在textbox1输入要识别的特征(以，分隔)，点击宠物推荐按钮进行查询。\n\n"
instruction2 = "宠物查询：在textbox1输入要查询的宠物，点击宠物查询按钮进行查询。\n\n"
instruction3 = "增添规则：在textbox1输入要增加的特征(以，分隔)，在textbox2中输入要增加的结果，点击增添规则按钮进行增加。\n\n"
instruction4 = "删除规则：在textbox1输入要删除的结果，点击删除规则按钮进行删除。\n\n"
instruction5 = "修改规则：在textbox1输入要修改规则的结果，在textbox2中输入要修改的规则，点击修改规则按钮进行修改。\n\n"
instruction6 = "退出系统：点击退出系统按钮进行退出。\n\n"
text = tkinter.Text(win)

#输入框与标签
Label(win, text="textbox1", font=("Cambria", 15, "bold"), fg='white', bg='black', ).pack()
entry1 = Entry(win)
entry1.pack(expand=True)
Label(win, text="textbox2", font=("Cambria", 15, "bold"), fg='white', bg='black', ).pack()
entry2 = Entry(win)
entry2.pack(expand=True)

#按钮
#Btn1 = Button(win, text="宠物推荐",  font=("Cambria", 15, "bold"), command=identify(df1, df2))
Btn1 = Button(win, text="宠物推荐",  font=("Cambria", 15, "bold"), command=lambda:identify(df1,df2))
Btn1.pack()
Btn2 = Button(win, text="宠物查询",  font=("Courier", 15, "bold"), command=lambda:rule(df1,df2))
Btn2.pack()
Btn3 = Button(win, text="增添规则",  font=("Courier", 15, "bold"), command=lambda:insert(df, excelFile))
Btn3.pack()
Btn4 = Button(win, text="删除规则", font=("Courier", 15, "bold"), command=lambda:delete(df, excelFile))
Btn4.pack()
Btn5 = Button(win, text="修改规则", font=("Courier", 15, "bold"), command=lambda:update(df, excelFile))
Btn5.pack()
Btn6 = Button(win, text="退出系统", font=("Courier", 15, "bold"), command=wayout)
Btn6.pack()
Btn7 = Button(win, text="clear", font=("Courier", 13), command=clear)
Btn7.pack()

text.pack()
text.insert(END, "使用指南\n\n")
text.insert(END, instruction1)
text.insert(END, instruction2)
text.insert(END, instruction3)
text.insert(END, instruction4)
text.insert(END, instruction5)
text.insert(END, instruction6)

print("欢迎使用")
win.mainloop()



'''
#print("欢迎使用" + re.sub(".xlsx", "", excelFile))
while(1):
    flag = input("请选择要使用的功能：\n1.根据特征进行识别\n2.根据结果输出特征\n3.更新规则\n0.退出程序\n")
    if int(flag) == 1:
        identify(df1, df2)
    elif int(flag) == 2:
        rule(df1, df2)
    elif int(flag) == 3:
        while(1):
            flag1 = input("请选择要使用的功能：\n1.删除规则\n2.修改规则\n3.添加规则\n0.退出当前菜单\n")
            if int(flag1) == 1:
                delete(df, excelFile)
            elif int(flag1) == 2:
                update(df, excelFile)
            elif int(flag1) == 3:
                insert(df, excelFile)
            elif int(flag1) == 0:
                break
    elif int(flag) == 0:
        break
'''
