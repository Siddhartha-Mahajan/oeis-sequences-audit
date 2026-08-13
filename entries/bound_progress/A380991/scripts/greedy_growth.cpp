#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>

struct Point{int x,y;};
static bool operator==(Point a,Point b){return a.x==b.x&&a.y==b.y;}
static bool operator<(Point a,Point b){return a.x<b.x||(a.x==b.x&&a.y<b.y);}
static std::uint64_t key(Point p){return (std::uint64_t)(std::uint32_t)p.x<<32|(std::uint32_t)p.y;}
static std::uint64_t dirkey(int dx,int dy){
    int g=std::gcd(std::abs(dx),std::abs(dy));dx/=g;dy/=g;
    if(dx<0||(dx==0&&dy<0)){dx=-dx;dy=-dy;}
    return (std::uint64_t)(std::uint32_t)dx<<32|(std::uint32_t)dy;
}

static bool valid(Point p,const std::vector<Point>& points,int cap){
    std::unordered_map<std::uint64_t,int> directions;
    directions.reserve(points.size()*2);
    for(Point q:points) if(++directions[dirkey(q.x-p.x,q.y-p.y)]>=cap) return false;
    return true;
}

int main(int argc,char**argv){
    int cap=argc>1?std::atoi(argv[1]):5;
    int trials=argc>2?std::atoi(argv[2]):20000;
    std::uint64_t seed=argc>3?std::stoull(argv[3]):380991;
    std::mt19937_64 rng(seed);
    std::vector<Point> best;
    const Point step[4]={{1,0},{-1,0},{0,1},{0,-1}};
    const std::vector<std::string> published4 = {
        "                 #", "                 #", "                ####",
        "       ###      #", "       # ##     #", "       #  #    ##",
        "      ##  #    #", "      #   ##   #", "      #    #  ##",
        "     ##    #  #", "     #     ## #", "     #      ###",
        "  ####", "    #", "    #"};
    for(int trial=0;trial<trials;++trial){
        std::vector<Point> points;
        if(cap>=5){
            for(int y=0;y<(int)published4.size();++y)
                for(int x=0;x<(int)published4[y].size();++x)
                    if(published4[y][x]=='#') points.push_back({x,y});
        }else points={{0,0}};
        std::unordered_set<std::uint64_t> occupied;
        for(Point p:points)occupied.insert(key(p));
        while(true){
            std::set<Point> boundary;
            for(Point p:points) for(Point d:step){Point q{p.x+d.x,p.y+d.y};if(!occupied.count(key(q)))boundary.insert(q);}
            std::vector<Point> choices;
            for(Point p:boundary) if(valid(p,points,cap)) choices.push_back(p);
            if(choices.empty())break;
            // Prefer candidates with several occupied neighbors, with a small
            // random component to explore different connected shapes.
            std::shuffle(choices.begin(),choices.end(),rng);
            int examine=std::min<int>(choices.size(),8); int pick=0,best_score=-1;
            for(int i=0;i<examine;++i){
                int score=0;for(Point d:step)if(occupied.count(key({choices[i].x+d.x,choices[i].y+d.y})))++score;
                if(score>best_score){best_score=score;pick=i;}
            }
            Point p=choices[pick];points.push_back(p);occupied.insert(key(p));
        }
        if(points.size()>best.size()){
            best=points;std::cerr<<"trial="<<trial<<" size="<<best.size()<<"\n";
        }
    }
    std::sort(best.begin(),best.end());
    std::cout<<"cap="<<cap<<" trials="<<trials<<" seed="<<seed<<" size="<<best.size()<<"\npoints=";
    for(Point p:best)std::cout<<'('<<p.x<<','<<p.y<<')';
    std::cout<<'\n';
}
