import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const C = { night:"#263b4b", paper:"#f4e5c7", gold:"#f8bd58", coral:"#df795b", teal:"#739b8a", brown:"#8b5d45", cream:"#fff0cf", ink:"#243746" };
const Lamp: React.FC<{x:number;y:number;s?:number}> = ({x,y,s=1}) => {
 const f=useCurrentFrame(); const glow=.25+.16*Math.sin(f*.22+x);
 return <g transform={`translate(${x} ${y}) scale(${s})`}><ellipse rx="42" ry="26" fill={C.gold} opacity={glow}/><path d="M-28 0 Q0 23 28 0 L19 14 Q0 24 -19 14Z" fill={C.coral} stroke={C.brown} strokeWidth="3"/><path d="M0 -4 C-18 -20 2 -39 0 -48 C22 -25 15 -12 0 -4Z" fill={C.gold}/><path d="M0 -9 C-8 -20 3 -29 2 -33 C13 -20 8 -12 0 -9Z" fill={C.cream}/></g>
};
const Person: React.FC<{x:number;y:number;scale?:number;cloth:string;hair?:string;pose?:number}> = ({x,y,scale=1,cloth,hair="#342b2b",pose=0}) => {
 const f=useCurrentFrame(); const bob=Math.sin(f*.12+x)*3;
 return <g transform={`translate(${x} ${y+bob}) scale(${scale})`}>
  <ellipse cx="0" cy="4" rx="43" ry="11" fill="#26313a" opacity=".22"/>
  <path d="M-27 -94 Q-38 -62 -32 -18 L-24 0 L24 0 L32 -18 Q38 -62 27 -94Z" fill={cloth} stroke={C.brown} strokeWidth="3"/>
  <path d="M-20 -16 L-17 45 L-4 45 L2 -7 L9 45 L22 45 L22 -16Z" fill={C.ink}/>
  <path d="M-28 -82 Q-52 -62 -42 -40 L-31 -42 L-15 -70 M28 -82 Q45 -62 37 -48 L25 -50 L16 -70" fill="none" stroke={cloth} strokeWidth="13" strokeLinecap="round"/>
  <circle cx="0" cy="-111" r="29" fill="#b97953" stroke={C.brown} strokeWidth="3"/>
  <path d="M-29 -114 Q-30 -145 0 -143 Q28 -142 29 -115 L17 -126 L-15 -126Z" fill={hair}/>
  <circle cx="-9" cy="-111" r="2.7" fill={C.ink}/><circle cx="9" cy="-111" r="2.7" fill={C.ink}/><path d={pose===2?"M-9 -99 Q0 -91 9 -99":"M-7 -98 Q0 -94 7 -98"} stroke={C.ink} strokeWidth="2.5" fill="none" strokeLinecap="round"/>
  {pose===1&&<path d="M28 -78 L48 -94" stroke="#b97953" strokeWidth="9" strokeLinecap="round"/>}
 </g>
};
const Stall: React.FC<{x:number;y:number;s?:number;accent:string}> = ({x,y,s=1,accent}) => <g transform={`translate(${x} ${y}) scale(${s})`}>
 <path d="M-170 0 L-135 -94 L135 -94 L170 0Z" fill={accent} stroke={C.brown} strokeWidth="7"/>{[-95,-32,32,95].map((v,i)=><path key={i} d={`M${v} -94 L${v+12} 0 L${v+43} 0 L${v+31} -94Z`} fill={i%2?C.paper:C.coral}/> )}
 <rect x="-145" y="0" width="290" height="180" fill={C.brown}/><rect x="-124" y="16" width="248" height="140" fill="#3a4547"/>
 {Array.from({length:8},(_,i)=><g key={i} transform={`translate(${-100+i*28} 65)`}><path d="M-10 0 Q0 -20 10 0 L8 25 L-8 25Z" fill={[C.gold,C.teal,C.coral][i%3]}/><ellipse cy="1" rx="12" ry="5" fill={C.cream}/></g>)}
 <path d="M-150 180 L-170 205 L170 205 L150 180Z" fill={accent} stroke={C.brown} strokeWidth="5"/>
 </g>;

export const DiwaliStory: React.FC = () => {
 const f=useCurrentFrame(); const {fps}=useVideoConfig();
 const sec=f/fps;
 const scene=sec<8?0:sec<18?1:sec<32?2:sec<48?3:4;
 const captions=[
  ["THE MARKET AT DUSK","As evening fell, the old bazaar glowed with a thousand little lights."],
  ["MEET MEERA","Meera had come to buy sweets. But one quiet stall caught her eye."],
  ["A LITTLE PROBLEM","An elderly potter had made beautiful diyas, yet hardly anyone stopped."],
  ["A BRIGHT IDEA","Meera arranged the lamps in a shining trail and called out to the crowd."],
  ["LIGHT SHINES FURTHER","Soon the stall was full of smiling customers. Meera learned that kindness can light up a whole street."]
 ][scene];
 const fade=interpolate(f,[0,18,1780,1800],[0,1,1,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const childX=scene===1?interpolate(f,[240,530],[1120,650],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}):scene===2?650:scene===3?interpolate(f,[960,1370],[650,390],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}):390;
 const showPeople=scene>0;
 return <AbsoluteFill style={{background:C.night,opacity:fade,fontFamily:"Georgia, serif",overflow:"hidden"}}>
  <svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position:"absolute",inset:0}}>
   <defs><linearGradient id="storysky" x1="0" y1="0" x2="0" y2="1"><stop stopColor="#20394b"/><stop offset="1" stopColor="#b87961"/></linearGradient><radialGradient id="warm"><stop stopColor="#ffe0a0" stopOpacity=".7"/><stop offset="1" stopColor="#ffe0a0" stopOpacity="0"/></radialGradient></defs>
   <rect width="1080" height="1920" fill="url(#storysky)"/><circle cx="850" cy="240" r="170" fill="url(#warm)"/><circle cx="850" cy="240" r="55" fill={C.cream} opacity=".8"/>
   {Array.from({length:35},(_,i)=><circle key={i} cx={(i*173+41)%1050+15} cy={(i*97+50)%650+30} r={i%3===0?4:2} fill={C.cream} opacity={.4+.5*Math.abs(Math.sin(f*.06+i))}/>)}
   <path d="M0 590 L90 500 L160 560 L250 470 L340 570 L440 490 L550 560 L670 470 L790 555 L910 465 L1080 550 L1080 1200 L0 1200Z" fill="#354d55" opacity=".75"/>
   {Array.from({length:7},(_,i)=><g key={i}><path d={`M${70+i*155} 0 L${70+i*155} ${170+(i%3)*60}`} stroke={C.paper} strokeWidth="3" opacity=".7"/><path d={`M${47+i*155} ${170+(i%3)*60} Q${70+i*155} ${130+(i%3)*60} ${93+i*155} ${170+(i%3)*60} L${87+i*155} ${220+(i%3)*60} Q${70+i*155} ${240+(i%3)*60} ${53+i*155} ${220+(i%3)*60}Z`} fill={i%2?C.coral:C.gold} stroke={C.paper} strokeWidth="3"/></g>)}
   <path d="M0 1030 Q540 900 1080 1035 L1080 1920 L0 1920Z" fill="#b77a5c"/>
   <path d="M0 1200 Q300 1120 550 1200 T1080 1170" fill="none" stroke="#f2c38d" strokeWidth="8" opacity=".6"/>
   <g opacity={scene===0?.75:1}><Stall x={235} y={1010} s={1.03} accent="#c86e58"/><Stall x={825} y={985} s={1.08} accent="#d9a24e"/></g>
   {scene>=2&&<g><Stall x={540} y={1160} s={.7} accent={C.teal}/><Person x={690} y={1395} scale={1.05} cloth="#7b8d72" pose={scene>=3?2:0}/></g>}
   {showPeople&&<Person x={childX} y={1510} scale={1.1} cloth="#e6a34e" pose={scene===3?1:0}/>}
   {scene>=3&&<g>{[390,490,590,690,790].map((x,i)=><Lamp key={i} x={x} y={1570+(i%2)*45} s={.75}/>)}</g>}
   {[[110,1510],[260,1620],[430,1510],[650,1630],[835,1515],[970,1640]].map(([x,y],i)=><Lamp key={i} x={x} y={y} s={.85}/>)}
   {scene===4&&<g>{Array.from({length:18},(_,i)=><circle key={i} cx={(i*91+f*1.3)%1080} cy={800+(i*73)%700} r={3+i%3} fill={C.gold} opacity=".85"/>)}</g>}
  </svg>
  <div style={{position:"absolute",top:85,left:60,right:60,textAlign:"center",color:C.cream,textShadow:"0 4px 20px #1a2730"}}>
   <div style={{fontSize:21,letterSpacing:7,marginBottom:18,opacity:.9}}>A WATERCOLOR STORY</div>
   <div style={{fontSize:61,fontWeight:700,lineHeight:1.05}}>Meera and the<br/>Little Lights</div>
  </div>
  <div style={{position:"absolute",bottom:105,left:55,right:55,textAlign:"center",padding:"28px 24px",borderRadius:28,background:"rgba(28,43,51,.76)",border:"1px solid rgba(255,240,207,.35)",color:C.cream}}>
   <div style={{fontSize:24,letterSpacing:3,marginBottom:14,color:C.gold}}>{captions[0]}</div>
   <div style={{fontSize:31,lineHeight:1.32}}>{captions[1]}</div>
  </div>
 </AbsoluteFill>;
};
