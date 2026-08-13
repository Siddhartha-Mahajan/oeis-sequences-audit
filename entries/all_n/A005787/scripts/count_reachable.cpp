#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

static uint64_t affine_truth(int d,int parameter){
    uint64_t out=0;int constant=(parameter>>d)&1;
    for(int x=0;x<(1<<d);x++)if((__builtin_parity((unsigned)(parameter&x))^constant))out|=1ULL<<x;
    return out;
}
static uint64_t combine(int d,int coordinate,uint64_t zero,uint64_t one){
    uint64_t out=0;
    for(int y=0;y<(1<<d);y++){
        int low=y&((1<<coordinate)-1),high=y>>coordinate;
        int x0=low|(high<<(coordinate+1));int x1=x0|(1<<coordinate);
        if((zero>>y)&1)out|=1ULL<<x0;if((one>>y)&1)out|=1ULL<<x1;
    }return out;
}
static uint64_t slice(int n,uint64_t f,int coordinate,int bit){
    uint64_t out=0;
    for(int y=0;y<(1<<(n-1));y++){
        int low=y&((1<<coordinate)-1),high=y>>coordinate;
        int x=low|(high<<(coordinate+1))|(bit<<coordinate);
        if((f>>x)&1)out|=1ULL<<y;
    }return out;
}
static uint64_t spread32(uint32_t value){
    uint64_t x=value;
    x=(x|(x<<16))&0x0000FFFF0000FFFFULL;
    x=(x|(x<<8))&0x00FF00FF00FF00FFULL;
    x=(x|(x<<4))&0x0F0F0F0F0F0F0F0FULL;
    x=(x|(x<<2))&0x3333333333333333ULL;
    x=(x|(x<<1))&0x5555555555555555ULL;
    return x;
}
static uint32_t slice6(uint64_t f,int coordinate,int bit){
    int width=1<<coordinate,step=2*width,outshift=0;
    uint64_t mask=width==32?0xFFFFFFFFULL:((1ULL<<width)-1);
    uint32_t out=0;
    for(int base=bit*width;base<64;base+=step){out|=(uint32_t)(((f>>base)&mask)<<outshift);outshift+=width;}
    return out;
}
static long long choose(int n,int k){
    if(k<0||k>n)return 0;long long v=1;for(int i=1;i<=k;i++)v=v*(n-k+i)/i;return v;
}

int main(){
    std::vector<std::vector<uint64_t>> families(6);
    families[0]={0};
    std::vector<std::unordered_set<uint64_t>> membership(6);
    membership[0].insert(0);
    for(int n=1;n<=5;n++){
        std::unordered_set<uint64_t> next;
        size_t rough=(size_t)n*families[n-1].size()*(1ULL<<n);next.reserve(rough);
        std::vector<uint64_t> aff;for(int p=0;p<(1<<n);p++)aff.push_back(affine_truth(n-1,p));
        for(int coordinate=0;coordinate<n;coordinate++)for(uint64_t g:families[n-1])for(uint64_t h:aff)
            next.insert(combine(n-1,coordinate,g,h));
        families[n].assign(next.begin(),next.end());membership[n]=std::move(next);
        std::cout<<"a("<<n<<")="<<families[n].size()<<"\n";
    }
    std::unordered_set<uint32_t> affine5;
    std::array<uint32_t,64> affine5_values{};
    for(int p=0;p<64;p++){affine5_values[p]=(uint32_t)affine_truth(5,p);affine5.insert(affine5_values[p]);}
    std::array<unsigned long long,7> histogram{};
    for(uint64_t g:families[5]){
        for(int h=0;h<64;h++){
            uint64_t f=spread32((uint32_t)g)|(spread32(affine5_values[h])<<1);
            int r=1;
            for(int coordinate=1;coordinate<6;coordinate++)
                if(membership[5].count(slice6(f,coordinate,0))&&affine5.count(slice6(f,coordinate,1)))r++;
            histogram[r]++;
        }
    }
    std::array<unsigned long long,7> intersection{};
    for(int k=1;k<=6;k++){
        unsigned long long numerator=0;
        for(int r=k;r<=6;r++)numerator+=histogram[r]*choose(r-1,k-1);
        assert(numerator%choose(5,k-1)==0);
        intersection[k]=numerator/choose(5,k-1);
        std::cout<<"I(6,"<<k<<")="<<intersection[k]<<"\n";
    }
    long long total=0;
    for(int k=1;k<=6;k++)total+=(k&1?1:-1)*choose(6,k)*(long long)intersection[k];
    std::cout<<"a(6)="<<total<<"\nE0_histogram";
    for(int r=1;r<=6;r++)std::cout<<" "<<r<<":"<<histogram[r];
    std::cout<<"\n";
}
