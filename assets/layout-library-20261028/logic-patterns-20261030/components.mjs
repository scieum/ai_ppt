import {C,shape,text} from '../recipes/components.mjs';
export {C,shape,text};
export function band(s,label,value,y=640){
 shape(s,'conclusion-band',150,y,980,40,'#1C130D','roundRect','#85501D');
 shape(s,'conclusion-tag',150,y,100,40,C.orange,'roundRect');
 text(s,'conclusion-tag-text',label,156,y+2,88,36,22,'#111111',true,'center');
 text(s,'conclusion-text',value,270,y+2,842,36,21,C.white,false,'left');
}
export function line(s,name,x,y,w,h=1){shape(s,name,x,y,w,h,'#666666','rect');}
export function stepCard(s,name,num,title,x){
 shape(s,name+'-card',x,352,300,260,'#242424','roundRect');
 shape(s,name+'-number-bg',x+22,374,30,30,C.orange,'ellipse');
 text(s,name+'-number',String(num),x+22,374,30,30,20,'#111111',true,'center');
 text(s,name+'-title',title,x+66,370,212,38,25,C.white,true);
}
export function compareRow(s,name,left,right,y){
 shape(s,name+'-left',150,y,470,70,'#241B17','roundRect');
 shape(s,name+'-right',660,y,470,70,'#171E24','roundRect');
 text(s,name+'-cross','×',174,y+13,38,44,34,'#BD7046',true,'center');
 text(s,name+'-left-text',left,227,y+13,370,44,23,'#C6C3C1');
 text(s,name+'-check','✓',684,y+17,38,36,30,'#9DC7F5',true,'center');
 text(s,name+'-right-text',right,737,y+13,370,44,23,C.white);
}
export function criteriaRow(s,name,values,y){
 const t=s.tables.add({rows:1,columns:3,left:270,top:y,width:900,height:54,columnWidths:[140,435,325],values:[values]});
 t.name=name;t.borders.assign({style:'solid',fill:'#000000',width:6});
 for(let c=0;c<3;c++){const cell=t.getCell(0,c);cell.fill=c===0?'#2C2C2C':c===1?'#202020':'#20272D';cell.text.style={typeface:'Pretendard',fontSize:c===2?20:22,color:c===0?C.orange:C.white,bold:c===0,verticalAlignment:'middle'};}
 return t;
}
