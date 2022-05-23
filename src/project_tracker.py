from IPython.display import HTML, display, Image, Markdown, FileLink, FileLinks
import os
import pandas as pd
from utils import find_in_list, recursive_glob, highlight_row, highlight_cell


def read_dd_proforma(li):
    '''
    li = list of fpths
    '''

    df = pd.DataFrame()

    def add_status(df,fpth):

        di = {
          'Group': 'Management',
          'Ref': 'ProformaFpth',
          'Value':fpth
        }
        di1 = {
          'Group': 'Management',
          'Ref': 'Status',
          'Value':os.path.basename(os.path.dirname(fpth))
        }
        df=df.append(di, ignore_index=True)
        df=df.append(di1, ignore_index=True)
        return df

    for n in range(0,len(li)):
        if n ==0:
            df=pd.read_excel(li[n])
            df=add_status(df,li[n])
            #df['Ref']=df['Ref'].str.replace(' ', '')
            df['Group']=df['Group'].str.replace(' ', '')
            df=df.set_index(['Group','Ref'])
            cols=list(df)
            col_name = list(df)[0]
            new = os.path.basename(li[n]).split('.')[0]
            df=df.rename(columns={col_name:new})
        else:
            tmp=pd.read_excel(li[n])
            tmp=add_status(tmp,li[n])
            tmp=tmp.set_index(['Group','Ref'])
            cols=list(tmp)
            col_name = list(tmp)[len(list(tmp))-1]
            new = os.path.basename(li[n]).split('.')[0]
            tmp=tmp.rename(columns={col_name:new})
            df[new]=tmp[new]

    return df

def list_folders_with_files(fdir,pattern):#NOT IN USE
    li=recursive_glob(rootdir=fdir, pattern=pattern, recursive=True)
    fol = [os.path.dirname(l) for l in li]
    return set(fol)

def list_folders(fdir):
    return [item for item in os.listdir(fdir) if os.path.isdir(os.path.join(fdir, item))]

def print_project_list(fpth,print_str='list of active projects:'):

    
    display(HTML('<h2>'+print_str+'</h2>'))
    print('------------------------')
    display(FileLinks(fpth,result_html_prefix='<h2>', result_html_suffix='</h2><br>'))
    print('')

def create_di(df,group_row,ref_col):
    '''
    creates a dict from a data frame row
    '''
    keys=df.loc[group_row].unique().tolist()
    di={}
    for key in keys:
        di[key] = list(df.loc[group_row].reset_index().set_index(group_row).loc[key][ref_col])
    return di
    
def compile_projects(rootdir, pattern='*.xlsx', fdir=''): #,fnm='_compiled.xlsx',,show=False
    
    def messylistremove(li,char="_"):
        rem=[]
        for l in li:
            if os.path.basename(l)[0] == char:
                rem.append(l)
            else:
                next
        for r in rem:
            li.remove(r)
        return li

    li = recursive_glob(rootdir=rootdir, pattern=pattern, recursive=True)
    li = messylistremove(li)
    li = messylistremove(li, char="~")
    if fdir != '':
        li = find_in_list(li, fdir)
    else:
        pass
    df = read_dd_proforma(li)
    # if show == True:
    #     display(Markdown('## compiled dataframe of projects:'))
    #     print('-------------------------------')
    df_out = df.reset_index().set_index('Ref').T
    di = create_di(df_out,'Group','Ref')
    df_out = df_out.drop(['Group'])
    
    #if show == True:
    #    display(table_toexcel(df_out,di,fpth=rootdir+'\\'+fnm,wrap=True,table_style='Table Style Light 8',filelink_format='h2'))#
    #else:
    #    table_toexcel(df_out, di, fpth=rootdir + '\\' + fnm, wrap=True, table_style='Table Style Light 8')
    return df, df_out

def project_summary(rootdir,pattern='*.*'):
    
    pattern='*.*'
    fols=list_folders(rootdir)
    display(HTML('<h1>'+'Click on links below for detailed project summaries:'+'</h1>'))
    for fol in fols:
        fdir =rootdir + '\\' + fol 
        print_str = 'list of projects '+str(fol)+':'
        print_project_list(fdir,print_str=print_str)
        
def make_strftime(df,cols):
    '''
    change datetime formatting for selected columns
    '''
    for n in range(0,len(df)):
        for col in cols:
            try:
                df[col].iat[n] = df[col].iat[n].strftime("%Y-%m-%d")
            except:
                pass
    return df



def exec_sum(df,print_str='',rows=['WorkType','Client / Originator','Brief','Budget','Start','Sign Off'],\
             highlight_row=True, show =True):
    if show ==True:
        print('')
        display(Markdown('## '+print_str))
        print('------------------')
    df1=df.reset_index().set_index('Ref')
    del df1['Group']
    df2=df1.T[rows].sort_values(by=['WorkType'])
    cols=['Sign Off','Start']
    df2=make_strftime(df2,cols)
    df2['Budget']=df2['Budget'].fillna(0)
    df2=df2.fillna('')

    colours={'Project Management':'background-color: #afbaff',
             'Engineering Analysis':'background-color: #f9b8b8',
             'Engineering Design':'background-color: #bfffc2',
             'Backend Development':'background-color: #e5baff',
             'Frontend Development':'background-color: #fbfcb8'}
    if show == True:
        if highlight_row == True:
          display((df2.style
          .apply(highlight, di=colours, col=['WorkType'], axis=1)
          .format({'Budget': '£{:,.0f}'})
              ))
        else:
          display((df2.style
          .applymap(highlight_cell,di=colours,subset=['WorkType'])
          .format({'Budget': '£{:,.0f}'})
              ))

    return df2

if __name__ == '__main__':
    if __debug__:
      #rootdir=os.getcwd()+'\\'+'projects'
      #rootdir=r'J:\J4321\DigitalDesignTeam\Management\ProjectTracker'+'\\'+'projects' 
      #df=compile_projects(rootdir)
      #print_str = 'Executive Summary of All Projects:'
      #exec_sum(df,print_str=print_str,rows=['WorkType','Status','Client / Originator','Brief','Budget','Start','Sign Off'],highlight_row = False)
      #project_summary(rootdir,pattern='*.*')
      #print('debug over')
      #import mf_scripts.project_tracker

      # import importlib
      # importlib.reload(mf_scripts.project_tracker)
      fdir = r'J:\J4321\DigitalDesignTeam\Management\engDevPlan\ProjectTracker\projects'
      print_str = 'Executive Summary of All Projects:'
      df = compile_projects(fdir)
      df1 = exec_sum(df, print_str=print_str,
                                                rows=['WorkType', 'Status', 'Client / Originator', 'Brief', 'Budget',
                                                      'Start', 'Sign Off'], highlight_row=False, show=False)
      print('debug over')
    else:
        print('im not in debug')