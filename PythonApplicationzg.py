#python3.6
#******************************************************
#Author:linuas
#Date of completion:2019-7-19
#This is a program for finding GADAG based on the DFS
#traversal low point algorithm
#******************************************************
import linecache

class Port():
    def __init__(self,spoint,dpoint,dire,dcircle,couldcircle=[]):#端口的源点、目的点、方向ew、目的环、可达环
        self.spoint=spoint
        self.dpoint=dpoint
        self.dire=dire
        self.dcircle=dcircle
        self.couldcircle=couldcircle
    def printinfo(self):
        print("********************************")
        print("端口原点："+str(self.spoint))
        print("去往："+str(self.dpoint))
        print("东西向："+str(self.dire))
        print("目的环："+str(self.dcircle))
        print("可达环："+str(self.couldcircle))
        print("********************************")

def remove_self(a):#去除自身重复元素且不改变顺序
    b=list(set(a))
    b.sort(key=a.index)
    return b
   

def remove_other(a,b):#在a中去除a和b的交集
    c=list(set(a)&set(b))#去除a列表中与b列表相同的节点
    for i in c:
          a.remove(i)


# def retu_partpoint(figure):#返回figure的割点
#     partpoint=[]
#     for item in figure:
#         if len(item)>1 and (item[0][0]==item[-1][-1] or item[1][0]==item[-1][-1]):
#             partpoint.append(item[-1][-1])
#     #partpoint.remove(root)
#     #partpoint=list(set(partpoint))
#     return partpoint


# 启动下面函数的
def retu_ringtree(ringtree,s):
    result=[]
    result.extend(ringtree[s])
    nowlist=ringtree[s]
    for i in nowlist:
        retu_list(ringtree,i,result)
    return result


# 检测能到达什么环
def retu_list(ringtree,d,result):
    for i in ringtree[d]:
        result.append(i)
        if len(ringtree[i])!=0:
            retu_list(ringtree,i,result)


def retu_2_tree(figure,s,d,tp_code):#返回s-d的两棵树,设计端口属性
    workpath=[]#工作路径
    protectpath=[]#保护路径
    n=len(tp_code)
    real_figure=[[]for i in range(n)]#真实的环
    share_point=[[i]for i in range(n+1)]#节点端口属性
    shareque=[]
    m=0
    for item in figure:
        if len(item)>1:
            real_figure[m].extend(item)
            m+=1
    for i in range(n-1,m-1,-1):
        del real_figure[i]


    circle_point=[[]for i in range(m)]#环绑定节点
    for i in range(m):
        for j in range(len(real_figure[i])):
            circle_point[i].append(real_figure[i][j][0])#链接的前端
        if i!=0:
            shareque.append(circle_point[i][0])
            del circle_point[i][0]#除了主环其他都是子环，开头去掉
        shareque.append(real_figure[i][-1][-1])

        if d in circle_point[i]:d_circle=i#目的环
        if s in circle_point[i]:s_circle=i#源环


    shareque=list(set(shareque)) # 去重

    # 构造环树
    ringtree=[[]for i in range(m)]
    for i in range(1,m):#环树
        for j in range(m):
            if real_figure[i][0][0] in circle_point[j]:
                midcircle3=j
                break
        ringtree[midcircle3].append(i)


    # 加端口属性
    for i in range(m):
        for j in range(len(real_figure[i])):
            for k in range(m):
                if real_figure[i][j][1] in circle_point[k]:midcircle1=k
                if real_figure[i][j][0] in circle_point[k]:midcircle2=k
            share_point[real_figure[i][j][0]].append(1)
            share_point[real_figure[i][j][0]][-1]=Port(real_figure[i][j][0],real_figure[i][j][1],'e',midcircle1,retu_ringtree(ringtree,midcircle1))
            share_point[real_figure[i][j][1]].append(1)
            share_point[real_figure[i][j][1]][-1]=Port(real_figure[i][j][1],real_figure[i][j][0],'w',midcircle2,retu_ringtree(ringtree,midcircle2))
############################################


#下面是用了端口属性的找树方式
    now_circle=s_circle#当前环从源环开始
    now_point=s
    flag=True#是否找到目的环
    while(now_circle!=d_circle):#workpath环间转发
        if now_point in shareque:
            for i in range(len(share_point[now_point])-1):
                if share_point[now_point][i+1].dcircle==d_circle and share_point[now_point][i+1].dire=='e':#共享节点目的环是目的环且方向为e
                    now_circle=d_circle
                    flag=False
                    break
            for i in range(len(share_point[now_point])-1):
                if d_circle in share_point[now_point][i+1].couldcircle and share_point[now_point][i+1].dire=='e' and flag:#可到达环
                    now_circle=share_point[now_point][i+1].dcircle
        for item in real_figure[now_circle]:
            if item[0]==now_point:
                workpath.append(item)
                now_point=item[1]
                break
    for item in real_figure[d_circle]:#workpath环上转发
        if item[0]==now_point:
            workpath.append(item)
            now_point=item[1]
        if item[1]==d:
            break
    print("工作路径:"+str(workpath))#工作路径***


#---------------------------------------------------------------
    now_circle=s_circle#当前环从源环开始
    now_point=s
    flag=True
    for item in real_figure:
        for itom in item:
            itom.reverse()
        item.reverse()
    while(now_circle!=d_circle):#protectpath环间转发
        if now_point in shareque:
            for i in range(len(share_point[now_point])-1):
                if share_point[now_point][i+1].dcircle==d_circle and share_point[now_point][i+1].dire=='w':#共享节点目的环是目的环且方向为w
                    now_circle=d_circle
                    flag=False
                    break
            for i in range(len(share_point[now_point])-1):
                if d_circle in share_point[now_point][i+1].couldcircle and share_point[now_point][i+1].dire=='w' and flag:#可到达环
                    now_circle=share_point[now_point][i+1].dcircle
        for item in real_figure[now_circle]:
            if item[0]==now_point:
                protectpath.append(item)
                now_point=item[1]
                break
    for item in real_figure[d_circle]:#protectpath环上转发
        if item[0]==now_point:
            protectpath.append(item)
            now_point=item[1]
        if item[1]==d:
            break
    print("保护路径:"+str(protectpath))#保护路径***
#上面是用了端口属性的找树方式


############################################
    for item in circle_point:
        print("环绑定节点"+str(item))
    print("共享节点"+str(shareque))
    print("------")
    for i in range(n+1):
        for j in range(1,len(share_point[i]),1):
            share_point[i][j].printinfo()
    print("-----环树")
    for item in ringtree:
        print(item)
    print("0环可到达："+str(retu_ringtree(ringtree,0)))


def print_figure(figure):#打印figure环
    m=0
    for i in range(len(figure)):
        if len(figure[i])>1:
            print('环'+str(m)+':'+str(figure[i])) 
            m+=1
    #print("cut point:"+str(retu_partpoint(figure)))
    retu_2_tree(figure,1,7,tp_code)


# # 按对角线分割(邻接表)
# def retu_real_figure(tp_code):#返回一个拓扑的实际链接点数
#     n=len(tp_code)
#     num=0
#     for item in tp_code:
#         if item.count(1)==0:
#             num+=1
#     real_n=n-num
#     k=0
#     real_tp_code=[[]for i in range(real_n)]
#     for i in range(n):
#         if tp_code[i].count(1)!=0 and i < real_n:
#             k=1
#             break
#         if tp_code[i].count(1)!=0 and i >=real_n:
#             k=-1
#             break
#     if k==0:print("ERROR!")
#     if k==1:
#         for i in range(real_n):
#             for j in range(real_n):
#                 real_tp_code[i].append(tp_code[i][j])
#     if k==-1:
#         for i in range(real_n,n):
#             for j in range(real_n,n):
#                 real_tp_code[i-real_n].append(tp_code[i][j])
#     #print(real_tp_code)
#     #return real_tp_code
#     return real_n


def test_connect(d,m,tp_code,x):#测试d,m的连通性！！
    fmax=pow(10,3)
    n=len(tp_code)
    midcode=[[]for i in range(n)]#不改变tp_code值
    dis=[fmax for i in range(n)]#d到各点的最短距离
    book=[0 for i in range(n)]#各节点的遍历与否
    for i in range(n):
        for j in range(n):
            if tp_code[i][j]==1:
                midcode[i].append(1)
            else:
                midcode[i].append(fmax)
    midcode[x-1][d-1]=midcode[x-1][m-1]=fmax
    midcode[d-1][x-1]=midcode[m-1][x-1]=fmax
    for i in range(n):
        dis[i]=midcode[d-1][i]
    book[d-1]=1
    for i in range(n-1):#若连通则存在最短路径
        min=fmax
        for j in range(n):
            if book[j]==0 and dis[j]<fmax:
                min=dis[j]
                u=j
        book[u]=1
        for v in range(n):
            if midcode[u][v]<fmax and dis[v]>(dis[u]+midcode[u][v]):
                dis[v]=dis[u]+midcode[u][v]
    if dis[m-1]==fmax:
        return True
    else:
        return False


def tp_result(tp_code,root):#找环算法主程序
    n=len(tp_code)
    #real_n=retu_real_figure(tp_code)
    real_n=n
    num=1
    result_que=[]#已遍历列表
    wait_que=[]#待遍历列表
    gadag=[]#含环节点列表
    dfs=[real_n-1]*n#桶表示各个节点的dfs值
    stuck=[[-1,0]for i in range(0,n+1)]#帮助wait列表加环的桶
    figure=[[]for i in range(49)]
    result_que.append(root)
    gadag.append(root)
    while(1):#主环第一封闭环
        #print("----")
        now=result_que[-1]
        #print(now)
        nnn=0#now的邻接数，为0则弹出now
        k=n
        for i in range(n):
            if tp_code[now-1][i]!=0 and result_que.count(i+1)==0:#或只有一个邻接？            ## 当前遍历的点的邻接的点并且该点不在已遍历节点列表中
                nnn+=1
                if i+1<k:k=i+1                                                                ## k代表当前遍历的点的dfs值最小的未被遍历的邻接点
        if nnn==0:#该节点没有其他邻接，则回弹
            x=-2#初始为-2，不行则-4，-6···
            just=0
            outnum=0
            while(1):
                for i in range(n):
                    if tp_code[result_que[x]-1][i]!=0 and result_que.count(i+1)==0:
                        result_que.append(result_que[x])#将上一跳加入到最后，完成遍历后去除重复以DFS唯一
                        just=1
                        break
                outnum+=1
                if just!=0:break
                x-=1
            #print("***"+str(outnum))
            for i in range(outnum):
                figure[0].pop(-1)#弹出环
                gadag.pop(-1)#弹出节点
            continue
        #print('***'+str(result_que))
        result_que.append(k)
        gadag.append(k)
        figure[0].append([now,k])
        for i in range(n):
            if tp_code[now-1][i]!=0 and result_que.count(i+1)==0 and k!=i+1:#中间节点的非最小邻接
                wait_que.append(i+1)
                if stuck[i+1][1]==0:
                    stuck[i+1][1]+=1
                    stuck[i+1][0]=now
        if tp_code[result_que[-1]-1][root-1]!=0 and len(result_que)>2 and result_que[-2]!=root:#至少三个节点为一个环
            figure[0].append([k,root])
            break
    result_que=remove_self(result_que)
    wait_que=remove_self(wait_que)#去除wait中重复的节点
    remove_other(wait_que,result_que)
    if len(result_que)==real_n:#若已遍历n个则直接完成
        k=-1
    #wait_que.sort()
    #print(figure[0])
    #print(result_que)
    #print(wait_que)
    while(len(result_que)!=real_n):#n个节点全部遍历才结束
        now=result_que[-1]#当前已遍历列表的最后一位
        nnn=0
        test=[]
        for i in range(n):
            if tp_code[now-1][i]!=0 and result_que.count(i+1)==0:
                nnn+=1
            if tp_code[now-1][i]!=0:
                test.append(i+1)
        rule=result_que[:]
        rule.extend([i for i in range(1,n+1)])
        rule=list(set(rule))
        test.sort(key=rule.index)
        if nnn==0 and tp_code[now-1][root-1]==0 and (len(test)==1 or test_connect(test[0],test[1],tp_code,now)):#该节点没有其他邻接，则回弹
            x=-2#初始为-2，不行则-4，-6···    
            just=0
            outnum=0
            while(1):
                for i in range(n):
                    if tp_code[result_que[x]-1][i]!=0 and result_que.count(i+1)==0:
                        result_que.append(result_que[x])#将上一跳加入到最后，完成遍历后去除重复以DFS唯一
                        just=1
                        break
                outnum+=1
                if just!=0:break
                x-=1
            for i in range(outnum):       
                figure[num].pop(-1)#弹出环
                gadag.pop(-1)#弹出节点
            continue
        beg=now
        now-=1#将编号转为下标
        mid_que=[]#当前节点邻接列表每次迭代都更新
        print('result'+str(result_que))
        print('wait'+str(wait_que))
        print('当前编号'+str(now+1))
        for i in range(n):
            if tp_code[now][i]!=0:
                mid_que.append(i+1)#当前节点的邻接节点
        mid_que.sort()
        print('邻接：'+str(mid_que))
        print(gadag)
        print('----------------------')
        list_cmp=list(set(result_que)&set(mid_que))
        list_len=list(set(gadag)&set(mid_que))
        if len(list_len)>1:
            for i in list_cmp:
                mid_que.remove(i)#去除mid列表中与result列表相同的节点
            wait_que.extend(mid_que)#将剩下的mid加入wait
            for j in mid_que:
                if stuck[j][1]==0:
                    stuck[j][1]+=1
                    stuck[j][0]=now
            wait_que=remove_self(wait_que)#去除wait中重复的节点
            #wait_que.sort()
            result_que.append(wait_que[0])#排序之后加入待遍历列表中编号最小节点
            gadag.append(wait_que[0])
            for j in range(n):#正序收尾
                if tp_code[now][j]!=0 and result_que.count(j+1)!=0 and len(figure[num])!=0:
                    figure[num].append([now+1,j+1])
                    break
            num+=1#增环
            for j in range(n-1,-1,-1):#倒序开头
                if tp_code[wait_que[0]-1][j]!=0 and result_que.count(j+1)!=0:
                    mid=j+1
                    break
            #mid=stuck[wait_que[0]][0]
            figure[num].append([mid,wait_que[0]])
        else:
            for i in list_cmp:
                mid_que.remove(i)#去除重复节点
            result_que.append(mid_que[0])
            gadag.append(mid_que[0])
            fin=mid_que[0]
            mid_que.pop(0)
            wait_que.extend(mid_que)
            wait_que=remove_self(wait_que)#去除wait中重复的节点
            figure[num].append([beg,fin])
            beg=fin
        result_que=remove_self(result_que)
        remove_other(wait_que,result_que)
    if k!=-1:
        mid=figure[num][-1][1]#最后一跳路径
        mid2=figure[num][-1][0]
        for j in range(n):#正序收尾
            if tp_code[mid-1][j]!=0 and result_que.count(j+1)!=0 and j+1!=mid2:
                figure[num].append([mid,j+1])
                break
    for i in range(real_n-1):#dfs值
        dfs[result_que[i]-1]=i
    #print('已遍历列表'+str(result_que))
    #print('DFS值'+str(dfs))
    #print_figure(figure)
    return figure   # 环图，二元列表


# def tp_circle(tp_code1,root1,tp_code2,root2,cut_edge):#2个子图的合并找环
#     figure_result=[[]for i in range(49)]
#     figure_num=0
#     figure1=tp_result(tp_code1,root1)
#     print("figure1:"),
#     print_figure(figure1)
#     figure2=tp_result(tp_code2,root2)
#     print("figure2:"),
#     print_figure(figure2)
#     print("cut edge length:"+str(len(cut_edge)))
#     for item in figure1:
#             if len(item)>1:
#                 figure_result[figure_num].extend(item)
#                 figure_num+=1
#     if len(cut_edge)==1:#一条割边
#         figure_result[figure_num].extend(cut_edge)
#         figure_num+=1
#         for item in figure2:
#             if len(item)>1:
#                 figure_result[figure_num].extend(item)
#                 figure_num+=1
#     if len(cut_edge)==2:#两条割边
#         figure_result[figure_num].extend([cut_edge[0]])
#         figure_result[figure_num].extend([[4,5]])
#         figure_result[figure_num].extend([cut_edge[1]])
#         figure_num+=1
#         for item in figure2:
#             if len(item)>1:
#                 figure_result[figure_num].extend(item)
#                 figure_num+=1
#     print("figure result:")
#     for item in figure_result:
#         if len(item)==1:
#             print("cut edge:"+str(item))
#         if len(item)>1:
#             print("circle:"+str(item))
#


if __name__ == '__main__':
#normal circle
    #a = linecache.getlines('demo1.txt')#demo1是13节点拓扑,demo2是6节点拓扑,demo3是8节点拓扑,demo4是6测试拓扑,demo5是割点拓扑
    #a = linecache.getlines('randomgraph.txt')#randomgraph是随机10点拓扑图
    #a = linecache.getlines('random30.txt')#random30是随机30点拓扑图
    #a = linecache.getlines('random50.txt')#random50是随机50点拓扑图
    #a = linecache.getlines('test30_2.txt')#test30_1,2,4,5是随机30点拓扑图
    a = linecache.getlines('MRTdemo.txt')#MRTdemo是MRT加边双树测试拓扑图         a是列表
    nn = len(a)
    tp_code=[[]for i in range(nn)]
    k=0
    for item in a:
        j=0
        while(len(tp_code[k])!=nn):
            tp_code[k].append(int(item[j]))#字符串转int
            j+=2#不读\t
        k+=1
    for item in tp_code:
        print(item)

    print_figure(tp_result(tp_code,1))#(拓扑，root)找环
    '''
    #test_connect(1,12,tp_code)
#sub figure comb
    tp_code1=[[0,1,1,0,0,0],
              [1,0,1,0,0,0],
              [1,1,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0]]
    tp_code2=[[0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,1,1],
              [0,0,0,1,0,1],
              [0,0,0,1,1,0]]
    cut_edge=[[2,4],[5,3]]
    #print(retu_real_figure(tp_code2))
    #tp_result(tp_code3,1)#(拓扑，root)找环
    tp_circle(tp_code1,1,tp_code2,4,cut_edge)#找合并图的环（子图1,root1,子图2,root2,割边）
    '''
    '''
#spf_lowpoint algo
    tp_code=[[0, 1, 1, 0, 0, 0, 0, 0],
             [1, 0, 1, 1, 0, 0, 0, 0],
             [1, 1, 0, 0, 1, 0, 0, 0],
             [0, 1, 0, 0, 1, 0, 0, 0],
             [0, 0, 1, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1],
             [0, 0, 0, 0, 0, 1, 0, 1],
             [0, 0, 0, 0, 0, 1, 1, 0]]
    tp_spf(tp_code,1)
    '''