#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <vector>

int main(int argc,char**argv){
    int n=argc>1?std::atoi(argv[1]):10, trials=argc>2?std::atoi(argv[2]):10000;
    std::uint64_t seed=argc>3?std::stoull(argv[3]):365910;
    std::vector<std::uint32_t> sets;
    for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)for(int c=b+1;c<n;++c)for(int d=c+1;d<n;++d)
        sets.push_back((1u<<a)|(1u<<b)|(1u<<c)|(1u<<d));
    int N=sets.size();std::vector<std::vector<int>> adj(N);
    for(int i=0;i<N;++i)for(int j=i+1;j<N;++j)if(__builtin_popcount(sets[i]&sets[j])>=2){adj[i].push_back(j);adj[j].push_back(i);}
    std::mt19937_64 rng(seed);int best=N;std::vector<int> bestcol;
    for(int trial=0;trial<trials;++trial){
        std::vector<int> col(N,-1);int used=0;
        for(int step=0;step<N;++step){
            int bestsat=-1,bestdeg=-1;std::vector<int> ties;
            for(int v=0;v<N;++v)if(col[v]<0){
                std::uint64_t mask=0;std::set<int> large;
                for(int w:adj[v])if(col[w]>=0){if(col[w]<64)mask|=1ull<<col[w];else large.insert(col[w]);}
                int sat=__builtin_popcountll(mask)+large.size(),deg=adj[v].size();
                if(sat>bestsat||(sat==bestsat&&deg>bestdeg)){bestsat=sat;bestdeg=deg;ties={v};}
                else if(sat==bestsat&&deg==bestdeg)ties.push_back(v);
            }
            int v=ties[rng()%ties.size()];std::vector<char> forbidden(used+1,false);
            for(int w:adj[v])if(col[w]>=0&&col[w]<=used)forbidden[col[w]]=true;
            std::vector<int> available;for(int c=0;c<used;++c)if(!forbidden[c])available.push_back(c);
            // Usually choose the smallest color; occasionally choose another
            // legal old color to diversify later saturation patterns.
            if(available.empty())col[v]=used++;
            else col[v]=available[(trial%7==0)?rng()%available.size():0];
        }
        if(used<best){best=used;bestcol=col;std::cerr<<"trial="<<trial<<" colors="<<best<<"\n";}
    }
    std::cout<<"n="<<n<<" trials="<<trials<<" seed="<<seed<<" colors="<<best<<"\n";
    for(int c=0;c<best;++c){std::cout<<"color "<<c<<':' ;for(int v=0;v<N;++v)if(bestcol[v]==c){
        std::cout<<" {";bool first=true;for(int b=0;b<n;++b)if(sets[v]&(1u<<b)){if(!first)std::cout<<',';std::cout<<b+1;first=false;}std::cout<<'}';
    }std::cout<<'\n';}
}
