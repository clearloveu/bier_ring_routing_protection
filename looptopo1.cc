//Author:sys
//Date of creation:2019-7-8
//This is a program for finding GADAG based on the DFS
//traversal low point algorithm
#include <iostream>
#include <map>
#include <vector>
#include <stack>
#include <string>
#include <algorithm>
#include <fstream>
#include <cmath>
#include <sstream>
#include <cstring>
using namespace std;


bool test_connect(int d,int m,vector<vector<int>> tp_code,int x){
	int fmax=pow(10,3);
	int n=tp_code.size();
	int midcode[n][n];
	int dis[n];
	int book[n];
	for(int i=0;i!=n;++i){
		memset(midcode[i],0,sizeof(midcode[i]));
	}
//	for(int i=0;i!=n;++i){
//		for(int j=0;j!=n;++j){
//			midcode[i][j]<<" ";
//		}
//		cout<<endl;
//	}
	memset(dis,fmax,sizeof(dis));
	memset(book,0,sizeof(book));

	for(int i=0;i!=n;++i){
		for(int j=0;j!=n;++j){
			if(tp_code[i][j]==1){
				midcode[i][j]=1;
			}else{
				midcode[i][j]=fmax;
			}
		}
	}
	midcode[x][m]=fmax;
	midcode[x][d]=fmax;

	midcode[d][x]=fmax;
	midcode[m][x]=fmax;
	int u=0;
	for(int i=0;i!=n;++i){
		dis[i]=midcode[d][i];
	}
	book[d]=1;
	for(int i=0;i!=n-1;++i){
		int min=fmax;
		for(int j=0;j!=n;++j){
			if(book[j]==0&&dis[j]<fmax){
				min=dis[j];
				u=j;
			}
		}
		book[u]=1;
		for(int v=0;v!=n;++v){
			if (midcode[u][v]<fmax&&dis[v]>(dis[u]+midcode[u][v])){
				dis[v]=dis[u]+midcode[u][v];
			}
		}
		cout<<"----"<<min<<"----"<<endl;
	}
	if(dis[m]==fmax){
		return true;
	}else{
		return false;
	}

}

//judge the array repetition
bool ischeap(vector<int>&a){
	vector<int> temp(a.size());
	for(int i=0;i!=(int)a.size();++i){
		temp[i]=0;
	}

	for(int i=0;i!=(int)a.size();++i){
		temp[a[i]]++;
	}
	for(int i=0;i!=(int)a.size();++i){
		if(temp[i]>=2){
			return true;
		}
	}
	return false;
}

struct rearray{
	rearray(int i,int j):first(i),second(j){}
	~rearray()=default;
	void print(){
		cout<<"["<<first<<","<<second<<"]";
	}
	int first;
	int second;
};






vector<int> remove_self(vector<int>a){
	vector<int>test(a.begin(),a.end());
	vector<int>::iterator it,it1;
	for(it=++test.begin();it!=test.end();){
		it1=find(test.begin(),it,*it);
		if(it1!=it)
			it=test.erase(it);
		else
			it++;
	}
	return test;
}

//remove same index between a and b
void remove_other(vector<int>&a,vector<int>&b){
	for(auto iter=a.begin();iter!=a.end();++iter){
		int temp=*iter;
		for(auto itor=b.begin();itor!=b.end();++itor){
			if(temp==(*itor)){
//				a.erase(iter);
				*iter=-1;
//				break;
			}
		}
	}

	vector<int> v;
	for(auto i:a){
		if(i!=-1){
			v.push_back(i);
		}
	}
	a.clear();
	a=v;

}

map<int,vector<rearray>> tp_result(vector< vector<int>> tp_code,int root){

	int num=1;
	int n=tp_code.size();
//	vector<int>dfs(n-1);//nodes' dfs value
	int dfs[n-1];
	memset(dfs,0,sizeof(dfs));
//	for(int i=0;i!=n-1;++i){
//		cout<<dfs[i]<<" ";
//	}
	vector<int> result_que;//nodes comepletely traveled
	vector<int> wait_que; //node wait to be traveled
	vector<int> gadag; //nodes who have ring
	map<int,vector<rearray>>figure;
	result_que.push_back(root);
	gadag.push_back(root);
	int k1=n;
	while(1){
		int now=result_que.back();
		int nnn=0;
		int k=n;
		for(int i=0;i!=n;++i){
			int nodenum=count(result_que.begin(),result_que.end(),i);
			if((tp_code[now][i]!=0)&&(nodenum==0)){
				nnn++;
				if(i<k){
					k=i;
				}
			}
		}
		if(nnn==0){
			int x=-2;
			int just=0;
			int outnum=0;
			while(1){
				for(int i=0;i!=n;++i){
					int nodenum=count(result_que.begin(),result_que.end(),i);
					if((tp_code[result_que[result_que.size()+x]][i]!=0)&&(nodenum==0)){
						result_que.push_back(result_que[result_que.size()+x]);
						just=1;
						break;
					}
				}
				outnum++;
				if(just!=0){
					break;
				}

				x--;
			}
			for(int i=0;i!=outnum;++i){
				figure[0].pop_back();
				gadag.pop_back();
			}
			continue;

		}
		result_que.push_back(k);
		gadag.push_back(k);
		rearray a1(now,k);
		figure[0].push_back(a1);
		for(int i=0;i!=n;++i){
			int nodenum=count(result_que.begin(),result_que.end(),i);
			if((tp_code[now][i]!=0)&&(nodenum==0)&&(k!=i)){
				wait_que.push_back(i);
			}
		}
		if ((tp_code[result_que[result_que.size()-1]][root]!=0)&&(result_que.size()>2)&&(result_que[result_que.size()-2]!=root)){
			rearray temp(k,root);
			figure[0].push_back(temp);
			break;
		}
	k1=k;
	}
	result_que=remove_self(result_que);
	wait_que=remove_self(wait_que);
	remove_other(wait_que,result_que);
	if((int)result_que.size()==n){
		k1=-1;
	}
	sort(wait_que.begin(),wait_que.end());



//	find the sub_rings
	int mid=0;
	while((int)result_que.size()<n||((int)result_que.size()==n&&ischeap(result_que))){
		int now=result_que.back();
		int nnn=0;
		vector<int>test;
		for(int i=0;i!=n;i++){
			int nodenum=count(result_que.begin(),result_que.end(),i);
			if((tp_code[now][i]!=0)&&(nodenum==0)){
				nnn++;
			}
			if(tp_code[now][i]!=0){
				test.push_back(i);
			}
		}
		vector<int>rule=result_que;
		for(int i=0;i!=n;++i){
			rule.push_back(i);
		}
		rule=remove_self(rule);
		vector<int>temp;
		for(auto iter=rule.begin();iter!=rule.end();++iter){
			for(unsigned i=0;i!=test.size();++i){
				if(*iter==test[i]){
					temp.push_back(test[i]);
				}
			}
		}
		test=temp;
//		for(auto i:result_que){
//			cout<<i<<" ";
//		}
//		cout<<endl;
//		for(auto i:test){
//			cout<<i<<" ";
//		}
//		cout<<endl;

		if(nnn==0&&tp_code[now][root]==0&&(test.size()==1||test_connect(test[0],test[1],tp_code,now))){
			int x=-2;
			int just=0;
			int outnum=0;
			while(1){
				for(int i=0;i!=n;++i){
					int nodenum=count(result_que.begin(),result_que.end(),i);
					if((tp_code[result_que[result_que.size()+x]][i]!=0)&&(nodenum==0)){
						result_que.push_back(result_que[result_que.size()+x]);
						just=1;
						break;
					}
				}
				outnum++;
				if(just!=0) {
					break;
				}

				x--;
			}
			for(int i=0;i!=outnum;++i){
				figure[num].pop_back();
				gadag.pop_back();
			}
			continue;
		}
		int beg=now;
		vector<int>mid_que;
		for(int i=0;i!=n;++i){
			if(tp_code[now][i]!=0)
				mid_que.push_back(i);
		}
		sort(mid_que.begin(),mid_que.end());
		vector<int> list_cmp;
		for(int i=0;i!=(int)result_que.size();++i){
			for(int j=0;j!=(int)mid_que.size();++j){
				if(result_que[i]==mid_que[j]){
					list_cmp.push_back(result_que[i]);
				}
			}
		}
		vector<int>list_len;
		for(int i=0;i!=(int)gadag.size();++i){
			for(int j=0;j!=(int)mid_que.size();++j){
				if(gadag[i]==mid_que[j]){
					list_len.push_back(gadag[i]);
				}
			}
		}
		if(list_len.size()>1){
			for(int i=0;i!=(int)list_cmp.size();++i){
				for(auto iter=mid_que.begin();iter!=mid_que.end();++iter){
					if(*iter==list_cmp[i]){
						mid_que.erase(iter);
						break;
					}
				}
			}
			for(auto iter=mid_que.begin();iter!=mid_que.end();++iter){
				wait_que.push_back(*iter);
			}
			wait_que=remove_self(wait_que);
			sort(wait_que.begin(),wait_que.end());
			result_que.push_back(wait_que[0]);
			gadag.push_back(wait_que[0]);
			for(int j=0;j!=n;++j){
				int nodenum=count(result_que.begin(),result_que.end(),j);
				if((tp_code[now][j]!=0)&&(nodenum!=0)&&(figure[num].size()!=0)){
					rearray temp(now,j);
					figure[num].push_back(temp);
					break;
				}
			}

			num++;//decrease the ring


			for(int j=n-1;j>=0;--j){
				int nodenum=count(result_que.begin(),result_que.end(),j);
				if(tp_code[wait_que[0]][j]!=0&&nodenum!=0){
					mid=j;
					break;
				}
			}
			rearray a2(mid,wait_que[0]);
			figure[num].push_back(a2);
		}else{
			for(int i=0;i!=(int)list_cmp.size();++i){
				for(auto iter=mid_que.begin();iter!=mid_que.end();++iter){
					if(*iter==list_cmp[i]){
						mid_que.erase(iter);
						break;
					}
				}
			}
			result_que.push_back(mid_que[0]);
			gadag.push_back(mid_que[0]);
			int fin=mid_que[0];
			mid_que.erase(mid_que.begin());
			for(auto i=mid_que.begin();i!=mid_que.end();++i){
				wait_que.push_back(*i);
			}
			wait_que=remove_self(wait_que);
			rearray a3(beg,fin);
			figure[num].push_back(a3);
			beg=fin;
		}
		result_que=remove_self(result_que);
	    remove_other(wait_que,result_que);
	}
//	for(auto i:result_que){
//		cout<<i<<" ";
//	}
//	cout<<endl;
	if(k1!=-1){
		mid=figure[num][figure[num].size()-1].second;
		int mid2=figure[num][figure[num].size()-1].first;
		for(int j=0;j!=n;++j){
			int nodenum=count(result_que.begin(),result_que.end(),j);
			if(tp_code[mid][j]!=0&&nodenum!=0&&j!=mid2){
				rearray temp(mid,j);
				figure[num].push_back(temp);
				break;
			}
		}
	}

	for(int i=0;i!=n-1;++i){
		dfs[result_que[i]]=i;
	}
//	for(int i=0;i!=n-1;++i){
//		cout<<dfs[i]<<" ";
//	}
//	cout<<endl;

	for(auto i=figure.begin();i!=figure.end();++i){
		if(i->second.size()<=1){
			figure.erase(i++);
		}
	}
	return figure;
}


vector< vector<int> > ReadTopo(string source_file_name){
	ifstream source_file;
	source_file.open (source_file_name.c_str(),ios::in);//open the file
	if (source_file.fail ())
		{
			std::cout<<"error:read file fail";
		}
	//to save the topo.
	vector< vector<int> >array;
	int i=0;
	int n_nodes=0;
	while(!source_file.eof()){
		string line;
		getline(source_file,line);
		if (line == "")
			{
					// std::cout<<"error:line == zero";
					break;
			}
		std::istringstream isl(line);
		int element;
		vector<int> row;
		int j=0;
		while(isl>>element){
			row.push_back(element);
			j++;
		}
		if(i==0){
			n_nodes=j;
		}
		if (j != n_nodes )
		{
			std::cout<<"ERROR: The number of rows is not equal to the number of columns! in the adjacency matrix";
		}
		else
		{
			array.push_back (row);
		}
		i++;
	}
	if (i != n_nodes)
		{
			std::cout<<"ERROR: The number of rows is not equal to the number of columns! in the adjacency matrix";
		}
	source_file.close();
	return array;
}

int main(int argc,char *argv[]){
	string loc="80/test30_4.txt";
	ifstream input(loc);	
	vector<vector<int>> topo=ReadTopo(loc);
	map<int,vector<rearray>> ring=tp_result(topo,0);
	cout<<"123";
	cout<<endl;
	cout<<ring.size();
	cout<<endl;
	for(auto iter=ring.begin();iter!=ring.end();++iter){
		for(auto itor=iter->second.begin();itor!=iter->second.end();++itor){
			itor->print();
		}
		cout<<endl;
	}

	return 0;
}
