import React from "react";
import {AbsoluteFill, Audio, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {dialogue} from "./dialogueData";

const C={ink:"#070b13",panel:"#101a2b",orange:"#ff9b45",blue:"#78c9ff",white:"#f4f5f7",muted:"#9aa8bb"};
const clamp={extrapolateLeft:"clamp" as const,extrapolateRight:"clamp" as const};
const Human:React.FC<{frame:number;fps:number;active:boolean}> = ({frame,fps,active})=>{
 const bob=Math.sin(frame/13)*3, gesture=active?Math.sin(frame/7)*7:0;
 return <g transform={`translate(0 ${bob})`}>
  <ellipse cx="360" cy="1090" rx="190" ry="28" fill="#02050a" opacity=".65"/>
  <path d="M245 1080 Q252 850 310 790 Q360 760 416 790 Q472 850 480 1080Z" fill="#263c55" stroke="#54708d" strokeWidth="4"/>
  <path d="M295 825 Q360 880 430 825 L450 1070 L275 1070Z" fill="#344d68"/>
  <path d="M310 840 L360 915 L411 840" fill="none" stroke="#d8e0e9" strokeWidth="8" opacity=".8"/>
  <path d={`M285 870 Q${250+gesture} 930 245 980`} stroke="#c98b67" strokeWidth="35" strokeLinecap="round" fill="none"/>
  <path d={`M430 870 Q${470+gesture} 920 480 965`} stroke="#c98b67" strokeWidth="35" strokeLinecap="round" fill="none"/>
  <circle cx="360" cy="690" r="116" fill="#c98b67"/>
  <path d="M248 680 Q238 560 350 550 Q460 550 475 660 Q420 610 365 620 Q300 615 248 680" fill="#25232a"/>
  <path d="M255 700 Q270 785 360 802 Q445 780 465 700 Q438 828 360 830 Q280 815 255 700" fill="#b8795d" opacity=".45"/>
  <ellipse cx="320" cy="700" rx="10" ry={active?13:9} fill="#171b24"/><ellipse cx="402" cy="700" rx="10" ry={active?13:9} fill="#171b24"/>
  <path d={active?"M333 752 Q360 777 389 750":"M340 755 Q360 762 380 755"} stroke="#6f3d38" strokeWidth="6" fill="none" strokeLinecap="round"/>
  <path d="M275 640 Q310 610 340 638 M385 638 Q420 610 445 640" stroke="#25232a" strokeWidth="13" fill="none" strokeLinecap="round"/>
 </g>
};
const Claude:React.FC<{frame:number;active:boolean}> = ({frame,active})=>{
 const bob=Math.sin(frame/16)*5, blink=(frame%137<6)?0.12:1;
 return <g transform={`translate(0 ${bob})`}>
  <ellipse cx="760" cy="1080" rx="155" ry="25" fill="#02050a" opacity=".65"/>
  <rect x="625" y="780" width="270" height="270" rx="54" fill="#e98238" stroke="#ffbf83" strokeWidth="5"/>
  <path d="M650 820 Q760 765 870 820" fill="none" stroke="#ffc28c" strokeWidth="8" opacity=".5"/>
  <rect x="680" y="875" width="38" height={active?10:38} rx="8" fill="#27212a" opacity={blink}/>
  <rect x="802" y="875" width="38" height={active?10:38} rx="8" fill="#27212a" opacity={blink}/>
  <path d={active?"M720 965 Q760 1000 800 965":"M730 970 Q760 980 790 970"} stroke="#542d27" strokeWidth="9" fill="none" strokeLinecap="round"/>
  <path d="M645 1040 L620 1100 M875 1040 L900 1100" stroke="#e98238" strokeWidth="25" strokeLinecap="round"/>
  <circle cx="760" cy="760" r="18" fill="#ffc28c" opacity=".8"/>
 </g>
};
const Environment:React.FC<{frame:number;speaker:string}> = ({frame,speaker})=>{
 const drift=interpolate(frame,[0,2200],[0,-90],clamp);
 return <svg viewBox="0 0 1080 1920" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
  <defs>
   <linearGradient id="bg" x2="1" y2="1"><stop stopColor="#080d18"/><stop offset=".55" stopColor="#17243a"/><stop offset="1" stopColor="#090e19"/></linearGradient>
   <radialGradient id="glow"><stop stopColor="#f28a43" stopOpacity=".24"/><stop offset="1" stopColor="#f28a43" stopOpacity="0"/></radialGradient>
   <linearGradient id="floor" x2="0" y2="1"><stop stopColor="#18263b"/><stop offset="1" stopColor="#080c14"/></linearGradient>
   <filter id="blur"><feGaussianBlur stdDeviation="34"/></filter>
  </defs>
  <rect width="1080" height="1920" fill="url(#bg)"/>
  <ellipse cx="760" cy="650" rx="450" ry="500" fill="url(#glow)"/>
  <g opacity=".45" stroke="#54708c" strokeWidth="2" fill="none">
   {Array.from({length:9},(_,i)=><path key={i} d={`M${80+i*118} 0 V700`} opacity=".18"/>)}
   <path d="M0 300 H1080 M0 520 H1080 M0 740 H1080"/>
  </g>
  <g transform={`translate(${drift} 0)`} opacity=".6">
   {[0,1,2,3].map(i=><g key={i} transform={`translate(${80+i*285} 360)`}>
    <rect width="210" height="280" rx="18" fill="#0b1422" stroke="#334e6b" strokeWidth="3"/>
    <rect x="18" y="22" width="174" height="12" rx="6" fill="#6cb8e8" opacity=".65"/>
    {[0,1,2,3,4].map(j=><rect key={j} x="18" y={62+j*35} width={80+(j*17)%90} height="7" rx="4" fill={j%2?"#e88a4b":"#5e91b8"} opacity=".65"/>)}
   </g>)}
  </g>
  <path d="M0 1220 Q540 1120 1080 1220 V1920 H0Z" fill="url(#floor)"/>
  <path d="M0 1280 Q540 1180 1080 1280" stroke="#39516b" strokeWidth="3" fill="none" opacity=".5"/>
  <g filter="url(#blur)"><ellipse cx="350" cy="1050" rx="190" ry="110" fill="#457fb1" opacity=".12"/><ellipse cx="800" cy="1050" rx="180" ry="120" fill="#e98238" opacity=".12"/></g>
  <Human frame={frame} fps={30} active={speaker==="human"}/>
  <Claude frame={frame} active={speaker==="claude"}/>
 </svg>
};
export const DialogueShort:React.FC=()=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig();
 const current=dialogue.findIndex((d)=>frame/fps>=d.start && frame/fps<d.end);
 const line=current>=0?dialogue[current]:null;
 const speaker=line?.speaker??"human";
 const reveal=spring({frame:Math.max(0,frame-(line?Math.round(line.start*fps):0)),fps,config:{damping:18,stiffness:120}});
 const scale=interpolate(reveal,[0,1],[.97,1]);
 const push=speaker==="human"?interpolate(frame,[0,900,1800],[1,1.045,1],clamp):interpolate(frame,[0,900,1800],[1.04,1,1.04],clamp);
 return <AbsoluteFill style={{background:C.ink,fontFamily:"Arial,Helvetica,sans-serif"}}>
  <AbsoluteFill style={{transform:`scale(${push})`}}><Environment frame={frame} speaker={speaker}/></AbsoluteFill>
  <AbsoluteFill style={{background:"linear-gradient(180deg,rgba(3,7,13,.06) 48%,rgba(3,7,13,.65) 100%)"}}/>
  <div style={{position:"absolute",top:78,left:72,right:72,display:"flex",justifyContent:"space-between",alignItems:"center"}}>
   <div style={{fontSize:23,letterSpacing:5,color:"#b8c6d7",fontWeight:700}}>HUMAN <span style={{color:"#65758a"}}> / </span> CLAUDE</div>
   <div style={{width:10,height:10,borderRadius:20,background:speaker==="claude"?C.orange:C.blue,boxShadow:`0 0 20px ${speaker==="claude"?C.orange:C.blue}`}}/>
  </div>
  <div style={{position:"absolute",left:72,right:72,bottom:205,display:"flex",flexDirection:"column",alignItems:speaker==="human"?"flex-start":"flex-end",transform:`scale(${scale})`,opacity:line?1:0}}>
   <div style={{fontSize:21,fontWeight:800,letterSpacing:4,color:speaker==="human"?C.blue:C.orange,marginBottom:18}}>{speaker==="human"?"HUMAN":"CLAUDE"}</div>
   <div style={{maxWidth:850,background:"rgba(7,13,23,.88)",border:`1px solid ${speaker==="human"?"rgba(120,201,255,.45)":"rgba(255,155,69,.45)"}`,borderRadius:26,padding:"28px 34px",boxShadow:"0 18px 60px rgba(0,0,0,.35)",color:C.white,fontSize:38,lineHeight:1.28,fontWeight:600,backdropFilter:"blur(12px)"}}>{line?.text}</div>
  </div>
  <div style={{position:"absolute",bottom:94,left:72,right:72,height:3,background:"rgba(255,255,255,.12)"}}>
   <div style={{height:"100%",width:`${interpolate(frame,[0,dialogue[dialogue.length-1].end*fps],[0,100],clamp)}%`,background:"linear-gradient(90deg,#78c9ff,#ff9b45)"}}/>
  </div>
  <Audio src={staticFile("dialogue-audio.m4a")}/>
 </AbsoluteFill>;
};
