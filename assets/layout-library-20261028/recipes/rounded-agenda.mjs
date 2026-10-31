import {text} from './components.mjs';
export function roundedAgendaContent(slide,{title='오늘은 이 순서로 진행합니다',labels=['기본\n이해','자료\n살펴보기','미리\n확인하기','정리와\n다음 단계']}={}){
 const commands=[
  {moveTo:{x:4.8,y:28.3}},
  {cubicBezTo:{x1:0,y1:14.5,x2:10.3,y2:0,x:25,y:0}},
  {lineTo:{x:303.6,y:0}},
  {cubicBezTo:{x1:312.4,y1:0,x2:320.3,y2:5.4,x:323.5,y:13.6}},
  {lineTo:{x:376,y:148.8}},
  {cubicBezTo:{x1:377.9,y1:153.7,x2:377.9,y2:159.3,x:376,y:164.2}},
  {lineTo:{x:323.5,y:299.4}},
  {cubicBezTo:{x1:320.3,y1:307.6,x2:312.4,y2:313,x:303.6,y:313}},
  {lineTo:{x:25,y:313}},
  {cubicBezTo:{x1:10.3,y1:313,x2:0,y2:298.5,x:4.8,y:284.7}},
  {lineTo:{x:46.6,y:163.5}},
  {cubicBezTo:{x1:48.2,y1:159,x2:48.2,y2:154,x:46.6,y:149.5}},
  {lineTo:{x:4.8,y:28.3}},{close:{}}
 ];
 text(slide,'slot-title',title,170,195,943,65,40,'#FFFFFF',true,'center');
 for(const[i,x]of[155.33,396.95,634.29,875.62].entries()){
  slide.shapes.add({name:'agenda-rounded-block-'+i,geometry:'custom',position:{left:x,top:328.67,width:251.96,height:208.67},fill:'#383838',line:{fill:'none',width:0},customPaths:[{width:378,height:313,commands}]});
  text(slide,'slot-step-number-'+i,'PART '+(i+1),x+76.67,382,170,30,20,'#FF9228',true,'left');
  const body=text(slide,'slot-step-'+i,labels[i],x+76.67,421,170,88,22,'#FFFFFF',true,'left');body.text.style={verticalAlignment:'top',lineSpacing:1};
 }
}
