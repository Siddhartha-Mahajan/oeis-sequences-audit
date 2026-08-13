#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

struct Point { int x, y; };
static constexpr Point MOVES[8] = {{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};

static Point operator+(Point a, Point b) { return {a.x+b.x,a.y+b.y}; }
static Point operator-(Point a, Point b) { return {a.x-b.x,a.y-b.y}; }
static bool operator==(Point a, Point b) { return a.x==b.x && a.y==b.y; }
static std::uint64_t key(Point p) { return (std::uint64_t)(std::uint32_t)p.x<<32 | (std::uint32_t)p.y; }
static long long cross(Point a, Point b, Point c) {
    return (long long)(b.x-a.x)*(c.y-a.y)-(long long)(b.y-a.y)*(c.x-a.x);
}
static bool between(int a,int b,int c) { return std::min(a,b)<=c && c<=std::max(a,b); }
static bool intersects(Point a, Point b, Point c, Point d) {
    long long x1=cross(a,b,c), x2=cross(a,b,d), x3=cross(c,d,a), x4=cross(c,d,b);
    if (((x1>0&&x2<0)||(x1<0&&x2>0)) && ((x3>0&&x4<0)||(x3<0&&x4>0))) return true;
    if (x1==0 && between(a.x,b.x,c.x) && between(a.y,b.y,c.y)) return true;
    if (x2==0 && between(a.x,b.x,d.x) && between(a.y,b.y,d.y)) return true;
    if (x3==0 && between(c.x,d.x,a.x) && between(c.y,d.y,a.y)) return true;
    if (x4==0 && between(c.x,d.x,b.x) && between(c.y,d.y,b.y)) return true;
    return false;
}
static int move_index(Point d) {
    for (int i=0;i<8;++i) if (MOVES[i]==d) return i;
    std::abort();
}
static Point transform(Point p,int t) {
    if (t&4) p.x=-p.x;
    int rotations=t&3;
    while(rotations--){ int x=p.x; p.x=-p.y; p.y=x; }
    return p;
}

class Counter {
public:
    explicit Counter(int length_):length(length_) {
        path.push_back({0,0}); path.push_back({1,2});
        visited.insert(key({0,0})); visited.insert(key({1,2}));
    }
    void run(){ dfs(); }
    std::size_t count()const{return canonical.size();}
    std::uint64_t rooted_count()const{return rooted;}
private:
    int length;
    std::vector<Point> path;
    std::unordered_set<std::uint64_t> visited;
    std::unordered_set<std::string> canonical;
    std::uint64_t rooted=0;

    bool clear_edge(Point a,Point b,bool closing)const{
        int last=(int)path.size()-2;
        for(int i=0;i<=last;++i){
            if(i==last) continue;
            if(closing && i==0) continue;
            if(intersects(a,b,path[i],path[i+1])) return false;
        }
        return true;
    }
    std::string canon()const{
        std::vector<Point> moves(length);
        for(int i=0;i<length-1;++i) moves[i]=path[i+1]-path[i];
        moves[length-1]=path[0]-path.back();
        std::string best(length,'9');
        for(int t=0;t<8;++t){
            std::vector<int> f(length),r(length);
            for(int i=0;i<length;++i) f[i]=move_index(transform(moves[i],t));
            for(int i=0;i<length;++i){ Point q=transform(moves[length-1-i],t); q={-q.x,-q.y}; r[i]=move_index(q); }
            for(const auto* seq:{&f,&r}) for(int shift=0;shift<length;++shift){
                std::string s; s.resize(length);
                for(int i=0;i<length;++i) s[i]=char('0'+(*seq)[(i+shift)%length]);
                if(s<best) best=s;
            }
        }
        return best;
    }
    void dfs(){
        Point here=path.back();
        int used=(int)path.size()-1;
        if(used==length-1){
            Point d=path[0]-here;
            bool knight=false; for(Point m:MOVES) if(m==d) knight=true;
            if(knight && clear_edge(here,path[0],true)){ ++rooted; canonical.insert(canon()); }
            return;
        }
        for(Point d:MOVES){
            Point next=here+d;
            auto k=key(next);
            if(visited.count(k) || !clear_edge(here,next,false)) continue;
            visited.insert(k); path.push_back(next); dfs(); path.pop_back(); visited.erase(k);
        }
    }
};

int main(int argc,char**argv){
    if(argc!=2){std::cerr<<"usage: count_polygons N\n";return 2;}
    int n=std::atoi(argv[1]); Counter c(2*n); c.run();
    std::cout<<"n="<<n<<" rooted_fixed_first="<<c.rooted_count()<<" inequivalent="<<c.count()<<'\n';
}
