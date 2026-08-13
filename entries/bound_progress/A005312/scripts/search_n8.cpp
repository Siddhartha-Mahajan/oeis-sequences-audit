#include <algorithm>
#include <array>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <random>

using Mat = std::array<std::array<int,8>,8>;

static long long determinant(const Mat& a) {
    long long m[8][8]{};
    for(int i=0;i<8;i++) for(int j=0;j<8;j++) m[i][j]=a[i][j];
    long long previous=1, sign=1;
    for(int k=0;k<7;k++) {
        int pivot=k;
        while(pivot<8 && m[pivot][k]==0) pivot++;
        if(pivot==8) return 0;
        if(pivot!=k){for(int j=0;j<8;j++)std::swap(m[k][j],m[pivot][j]);sign=-sign;}
        long long value=m[k][k];
        for(int i=k+1;i<8;i++) for(int j=k+1;j<8;j++)
            m[i][j]=(m[i][j]*value-m[i][k]*m[k][j])/previous;
        previous=value;
    }
    return sign*m[7][7];
}

static long double objective(const Mat& a) {
    if(determinant(a)==0) return -1;
    long double m[8][16]{};
    for(int i=0;i<8;i++) for(int j=0;j<8;j++) m[i][j]=a[i][j];
    for(int i=0;i<8;i++) m[i][8+i]=1;
    for(int c=0;c<8;c++) {
        int pivot=c;
        for(int r=c+1;r<8;r++) if(fabsl(m[r][c])>fabsl(m[pivot][c])) pivot=r;
        if(fabsl(m[pivot][c])<1e-30L) return -1;
        for(int j=0;j<16;j++) std::swap(m[c][j],m[pivot][j]);
        long double d=m[c][c];
        for(int j=0;j<16;j++) m[c][j]/=d;
        for(int r=0;r<8;r++) if(r!=c) {
            long double f=m[r][c];
            for(int j=0;j<16;j++) m[r][j]-=f*m[c][j];
        }
    }
    long double ans=0;
    for(int i=0;i<8;i++) for(int j=0;j<8;j++) ans+=m[i][8+j]*m[i][8+j];
    return ans;
}

int main(int argc,char**argv){
    long long steps=argc>1?std::stoll(argv[1]):2000000;
    uint64_t seed=argc>2?std::stoull(argv[2]):5312;
    std::mt19937_64 rng(seed);
    Mat cur{},best{};
    long double cs=-1,bs=-1;
    while(cs<0){for(int i=0;i<8;i++)for(int j=i;j<8;j++)cur[i][j]=cur[j][i]=rng()&1;cs=objective(cur);}
    best=cur;bs=cs;
    std::array<std::pair<int,int>,36> positions{}; int z=0;
    for(int i=0;i<8;i++)for(int j=i;j<8;j++)positions[z++]={i,j};
    for(long long it=0;it<steps;it++){
        if(it && it%10000==0){cur=best;cs=bs;}
        auto [i,j]=positions[rng()%36];cur[i][j]^=1;if(i!=j)cur[j][i]^=1;
        long double ns=objective(cur);
        long double temp=std::max(0.005L,0.35L*(1.0L-(it%10000)/10000.0L));
        bool accept=ns>0 && (ns>=cs || std::generate_canonical<long double,64>(rng)<expl((logl(ns)-logl(cs))/temp));
        if(accept)cs=ns;else{cur[i][j]^=1;if(i!=j)cur[j][i]^=1;}
        if(ns>bs){best=cur;bs=ns;std::cerr<<"best "<<std::setprecision(18)<<(double)bs<<" at "<<it<<"\n";}
    }
    std::cout<<"floating_objective "<<std::setprecision(20)<<(double)bs<<"\n";
    for(auto&r:best){for(int x:r)std::cout<<x;std::cout<<"\n";}
}
