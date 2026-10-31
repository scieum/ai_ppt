import {shape,text} from '../recipes/components.mjs';
// User-selected reference: left colored label, straight inner edge,
// near-black tinted body and a thin outline; no detached label pill.
export function conclusionBar(slide,value,{x=150,y=640,width=980,height=40}={}){
 shape(slide,'conclusion-bar-body',x,y,width,height,'#130B05','roundRect','#A95D19');
 shape(slide,'conclusion-bar-label-bg',x,y,88,height,'#E87C18','roundRect');
 shape(slide,'conclusion-bar-label-square-edge',x+73,y,15,height,'#E87C18','rect');
 text(slide,'conclusion-bar-label','결론',x+8,y+2,72,height-4,23,'#FFFFFF',true,'center');
 text(slide,'conclusion-bar-message',value,x+104,y+2,width-120,height-4,21,'#FFFFFF',false,'left');
}
