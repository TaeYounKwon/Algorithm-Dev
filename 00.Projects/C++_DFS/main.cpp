#include <iostream>
#include <vector>
using namespace std;


bool visited[10];
vector<int> graphDFS[10];

void dfs(int val){
    if(visited[val])
        return;

    visited[val]=true;
    cout<<val<<" ";
    for(int i=0; i<graphDFS[val].size(); i++){
        int currentVal=graphDFS[val][i];
        dfs(currentVal);
    }

}

start<int> s;
s.push(val);
markVisit[val]=true;
while(!s.empty()){
int currentVal= s.front();
s.pop();
cout<<currentVal<<"->";
for(int i=0; i<graphDFS[currentVal].size(); i++){
int closeNode=graphDFS[currentVal][i];
if(!isit[closeNode]){
q.push(closeNode);
markVisit[closeNode]=true;
}
}
}


int main() {
    graphDFS[1].push_back(2);
    graphDFS[1].push_back(3);
    graphDFS[2].push_back(4);
    graphDFS[2].push_back(5);
    graphDFS[3].push_back(6);
    dfs(1);
    return 0;
}
