export const C={bg:'#000000',card:'#202020',alt:'#2C2C2C',orange:'#FF9228',muted:'#AAAAAA',white:'#FFFFFF',line:'#414141'};
let seq=0;
export function shape(s,name,x,y,w,h,fill=C.card,g='roundRect',stroke='none'){
 return s.shapes.add({name,geometry:g,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:stroke==='none'?0:1}});
}
export function text(s,name,value,x,y,w,h,size=22,color=C.white,bold=false,align='left'){
 const sh=shape(s,name,x,y,w,h,'none','textbox');sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size,color,bold,alignment:align,verticalAlignment:'middle',wrap:true};sh.text.insets=0;return sh;
}
export function panel(s,name,x,y,w,h,label,desc){shape(s,name+'-bg',x,y,w,h);if(label)text(s,name+'-label',label,x+18,y+18,w-36,35,24,C.white,true,'center');if(desc)text(s,name+'-desc',desc,x+18,y+64,w-36,h-80,20,C.muted,false,'center');}
export function arrow(s,name,x,y,w=20,h=28){shape(s,name,x,y,w,h,C.orange,'chevron');}
export function imageSlot(s,name,x,y,w,h,label='이미지·화면 슬롯'){shape(s,name+'-frame',x,y,w,h,'#151515','roundRect','#555555');text(s,name,label,x+16,y+16,w-32,h-32,20,C.muted,false,'center');}
export function smallTag(s,name,value,x,y,w=110){shape(s,name+'-bg',x,y,w,28,'#3A2A1C');text(s,name,value,x+5,y,w-10,28,15,C.orange,true,'center');}
