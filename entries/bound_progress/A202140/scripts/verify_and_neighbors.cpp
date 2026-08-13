#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

using Matrix = std::uint32_t;
static constexpr Matrix MASK = (Matrix(1) << 25) - 1;

static std::array<std::uint8_t,32> images(Matrix b){
    std::uint8_t row[5]; for(int i=0;i<5;++i) row[i]=(b>>(5*i))&31;
    std::array<std::uint8_t,32> out{};
    for(int m=1;m<32;++m){int bit=__builtin_ctz(m);out[m]=out[m^(1<<bit)]|row[bit];}
    return out;
}
static Matrix multiply_right(Matrix a,const std::array<std::uint8_t,32>& image){
    Matrix out=0; for(int i=0;i<5;++i) out|=Matrix(image[(a>>(5*i))&31])<<(5*i); return out;
}
static Matrix rows(std::initializer_list<const char*> rs){
    Matrix m=0; int i=0; for(auto s:rs){for(int j=0;j<5;++j) if(s[j]=='1')m|=Matrix(1)<<(5*i+j);++i;}return m;
}
static std::string bits(Matrix m){std::string s;for(int i=0;i<5;++i){if(i)s+='/';for(int j=0;j<5;++j)s+=((m>>(5*i+j))&1)?'1':'0';}return s;}

class Closure{
public:
    Closure():seen(1u<<25,0){queue.reserve(8000000);}
    std::size_t size(std::array<Matrix,2> g){
        if(++stamp==0){std::fill(seen.begin(),seen.end(),0);stamp=1;}
        auto a=images(g[0]),b=images(g[1]);queue.clear();add(g[0]);add(g[1]);
        for(std::size_t h=0;h<queue.size();++h){Matrix x=queue[h];add(multiply_right(x,a));add(multiply_right(x,b));}
        return queue.size();
    }
private:
    std::vector<std::uint8_t> seen; std::uint8_t stamp=0; std::vector<Matrix> queue;
    void add(Matrix x){x&=MASK;if(seen[x]!=stamp){seen[x]=stamp;queue.push_back(x);}}
};

int main(){
    std::array<Matrix,2> published={
        rows({"00001","10000","01000","00100","00010"}),
        rows({"00100","11000","01000","00010","00001"})};
    Closure closure; auto baseline=closure.size(published); auto best=published; auto best_size=baseline;
    for(int which=0;which<2;++which) for(int bit=0;bit<25;++bit){
        auto candidate=published;candidate[which]^=Matrix(1)<<bit;
        auto score=closure.size(candidate);
        if(score>best_size){best=candidate;best_size=score;std::cerr<<"improvement "<<score<<"\n";}
    }
    for(int p=0;p<50;++p) for(int q=p+1;q<50;++q){
        auto candidate=published;
        candidate[p/25]^=Matrix(1)<<(p%25);
        candidate[q/25]^=Matrix(1)<<(q%25);
        auto score=closure.size(candidate);
        if(score>best_size){best=candidate;best_size=score;std::cerr<<"improvement "<<score<<"\n";}
    }
    std::cout<<"published="<<baseline<<"\nbest_radius_two_neighbor="<<best_size
             <<"\ng0="<<bits(best[0])<<"\ng1="<<bits(best[1])<<"\n";
}
