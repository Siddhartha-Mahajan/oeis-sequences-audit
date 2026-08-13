#include <algorithm>
#include <bit>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

static u64 gcd64(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static u64 mulmod(u64 a,u64 b,u64 m){return (u128)a*b%m;}
static u64 powmod(u64 a,u64 e,u64 m){u64 r=1;for(;e;e>>=1,a=mulmod(a,a,m))if(e&1)r=mulmod(r,a,m);return r;}
static bool prime(u64 n){
    if(n<2)return false;
    for(u64 p:{2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL}){
        if(n%p==0)return n==p;
    }
    u64 d=n-1,s=0;while(!(d&1)){d>>=1;++s;}
    for(u64 a:{2ULL,325ULL,9375ULL,28178ULL,450775ULL,9780504ULL,1795265022ULL}){
        if(a%n==0)continue;u64 x=powmod(a%n,d,n);if(x==1||x==n-1)continue;
        bool composite=true;for(u64 r=1;r<s;++r){x=mulmod(x,x,n);if(x==n-1){composite=false;break;}}
        if(composite)return false;
    }return true;
}
static u64 rho(u64 n){
    if(!(n&1))return 2;if(n%3==0)return 3;
    static std::mt19937_64 gen(0xA273354ULL);
    for(;;){u64 c=gen()%(n-1)+1,x=gen()%(n-2)+2,y=x,d=1;
        while(d==1){x=(mulmod(x,x,n)+c)%n;y=(mulmod(y,y,n)+c)%n;y=(mulmod(y,y,n)+c)%n;d=gcd64(x>y?x-y:y-x,n);}
        if(d!=n)return d;
    }
}
static void factor_rec(u64 n,std::vector<u64>&f){if(n==1)return;if(prime(n)){f.push_back(n);return;}u64 d=rho(n);factor_rec(d,f);factor_rec(n/d,f);}
static u64 isqrt(u64 n){u64 x=(u64)std::sqrt((long double)n);while((u128)(x+1)*(x+1)<=n)++x;while((u128)x*x>n)--x;return x;}
static u64 icbrt(u64 n){u64 x=(u64)std::cbrt((long double)n);while((u128)(x+1)*(x+1)*(x+1)<=n)++x;while((u128)x*x*x>n)--x;return x;}

using Factors=std::vector<std::pair<u64,unsigned>>;
static Factors factor(u64 n){std::vector<u64>raw;factor_rec(n,raw);std::sort(raw.begin(),raw.end());Factors f;for(std::size_t i=0;i<raw.size();){std::size_t j=i+1;while(j<raw.size()&&raw[j]==raw[i])++j;f.push_back({raw[i],(unsigned)(j-i)});i=j;}return f;}
static u64 square_pairs(u64 n,const Factors&f){u64 P=1;for(auto[p,e]:f){if(p%4==3&&(e&1))return 0;if(p%4==1)P*=e+1;}bool sq=isqrt(n)*isqrt(n)==n;bool twice=n%2==0&&isqrt(n/2)*isqrt(n/2)==n/2;return (P-sq+twice)/2;}
static void divisor_rec(const Factors&f,std::size_t i,u64 v,std::vector<u64>&out){if(i==f.size()){out.push_back(v);return;}auto[p,e]=f[i];for(unsigned j=0;j<=e;++j){divisor_rec(f,i+1,v,out);if(j<e)v*=p;}}
static std::vector<std::pair<u64,u64>> cube_pairs(u64 n,const Factors&f){
    std::vector<u64>ds;divisor_rec(f,0,1,ds);std::vector<std::pair<u64,u64>>out;
    for(u64 d:ds){u64 nd=n/d;if((u128)4*nd<(u128)d*d)continue;u128 q=(u128)4*nd-(u128)d*d;if(q%3)continue;u64 delta2=(u64)(q/3),delta=isqrt(delta2);if(delta*delta!=delta2||((d-delta)&1))continue;u64 x=(d-delta)/2,y=(d+delta)/2;if(x>=1&&x<=y&&(u128)x*x*x+(u128)y*y*y==n)out.push_back({x,y});}
    std::sort(out.begin(),out.end());out.erase(std::unique(out.begin(),out.end()),out.end());return out;
}
static std::string factor_json(const Factors&f){std::string s="[";for(std::size_t i=0;i<f.size();++i){if(i)s+=",";s+="["+std::to_string(f[i].first)+","+std::to_string(f[i].second)+"]";}return s+"]";}
static std::string pairs_json(const std::vector<std::pair<u64,u64>>&v){std::string s="[";for(std::size_t i=0;i<v.size();++i){if(i)s+=",";s+="["+std::to_string(v[i].first)+","+std::to_string(v[i].second)+"]";}return s+"]";}

int main(int argc,char**argv){
    if(argc!=4){std::cerr<<"usage: analyze_primitive_scalings BFILE EXCLUSIVE_LIMIT JSON_OUT\n";return 2;}
    const u64 limit=std::stoull(argv[2]);std::ifstream in(argv[1]);if(!in){std::cerr<<"cannot open b-file\n";return 2;}
    std::vector<u64>primitive;std::string line;while(std::getline(in,line)){if(line.empty()||line[0]=='#')continue;std::istringstream ss(line);u64 i,v;if(ss>>i>>v&&v<limit)primitive.push_back(v);}
    std::unordered_set<u64>seen;for(u64 m:primitive){u64 top=icbrt((limit-1)/m);for(u64 k=1;k<=top;++k)seen.insert((u64)((u128)m*k*k*k));}
    std::vector<u64>values(seen.begin(),seen.end());std::sort(values.begin(),values.end());
    std::ofstream factor_certificate(std::string(argv[3])+".factors.tsv");
    factor_certificate<<"# value\tprime_factorization\tpositive_square_pairs\n";
    struct Hit{u64 n,sq;Factors f;std::vector<std::pair<u64,u64>> cp;};std::vector<Hit>square3,solutions;
    for(std::size_t idx=0;idx<values.size();++idx){u64 n=values[idx];Factors f=factor(n);u64 sq=square_pairs(n,f);
        factor_certificate<<n<<'\t';for(std::size_t j=0;j<f.size();++j){if(j)factor_certificate<<',';factor_certificate<<f[j].first<<'^'<<f[j].second;}factor_certificate<<'\t'<<sq<<'\n';
        if(sq==3){auto cp=cube_pairs(n,f);square3.push_back({n,sq,f,cp});if(cp.size()==3)solutions.push_back(square3.back());}
        if((idx+1)%10000==0)std::cerr<<"processed "<<(idx+1)<<" / "<<values.size()<<"\n";
    }
    std::string j="{\n  \"exclusive_limit\": "+std::to_string(limit)+",\n  \"primitive_bases_below_limit\": "+std::to_string(primitive.size())+",\n  \"distinct_primitive_cube_scalings\": "+std::to_string(values.size())+",\n  \"square_multiplicity_three_candidates\": [\n";
    for(std::size_t i=0;i<square3.size();++i){auto&h=square3[i];j+="    {\"value\":"+std::to_string(h.n)+",\"factorization\":"+factor_json(h.f)+",\"cube_pairs\":"+pairs_json(h.cp)+"}"+(i+1==square3.size()?"\n":",\n");}
    j+="  ],\n  \"solutions_below_limit\": [";for(std::size_t i=0;i<solutions.size();++i){if(i)j+=",";j+=std::to_string(solutions[i].n);}j+="]\n}\n";std::ofstream out(argv[3]);out<<j;std::cout<<"primitive="<<primitive.size()<<" values="<<values.size()<<" square3="<<square3.size()<<" solutions="<<solutions.size()<<"\n";
}
