import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const colors = {
  night: "#263b4b", indigo: "#304c5b", paper: "#f4e5c7", gold: "#f8bd58",
  coral: "#df795b", teal: "#739b8a", brown: "#8b5d45", cream: "#fff0cf"
};

const Lamp: React.FC<{x:number;y:number;scale?:number;delay?:number}> = ({x,y,scale=1,delay=0}) => {
  const f = useCurrentFrame();
  const glow = 0.25 + 0.15 * Math.sin((f+delay)*0.22);
  return <g transform={`translate(${x} ${y}) scale(${scale})`}>
    <ellipse cx="0" cy="0" rx="45" ry="30" fill={colors.gold} opacity={glow}/>
    <path d="M-28 0 Q0 25 28 0 L20 14 Q0 26 -20 14Z" fill={colors.coral} stroke={colors.brown} strokeWidth="3"/>
    <path d="M0 -4 C-18 -20 2 -39 0 -48 C22 -25 15 -12 0 -4Z" fill={colors.gold}/>
    <path d="M0 -9 C-8 -20 3 -29 2 -33 C13 -20 8 -12 0 -9Z" fill={colors.cream}/>
  </g>;
};

const Star: React.FC<{x:number;y:number;r:number;phase:number}> = ({x,y,r,phase}) => {
  const f = useCurrentFrame();
  const op = 0.45 + 0.45 * Math.abs(Math.sin((f+phase)*0.08));
  return <circle cx={x} cy={y} r={r} fill={colors.cream} opacity={op}/>;
};

const MarketStall: React.FC<{x:number;y:number;scale?:number;accent:string}> = ({x,y,scale=1,accent}) => (
  <g transform={`translate(${x} ${y}) scale(${scale})`}>
    <path d="M-155 0 L-120 -95 L120 -95 L155 0Z" fill={accent} stroke={colors.brown} strokeWidth="7" strokeLinejoin="round"/>
    {[-90,-30,30,90].map((v,i)=><path key={i} d={`M${v} -95 L${v+12} 0 L${v+42} 0 L${v+30} -95Z`} fill={i%2?colors.paper:colors.coral} opacity=".9"/>)}
    <rect x="-130" y="0" width="260" height="180" rx="5" fill={colors.brown}/>
    <rect x="-112" y="18" width="224" height="145" fill={colors.night}/>
    {Array.from({length:7},(_,i)=><g key={i} transform={`translate(${-90+i*30} 58)`}><circle r="11" fill={[colors.gold,colors.teal,colors.coral][i%3]}/><path d="M-9 9 L9 9 L6 32 L-6 32Z" fill={colors.paper}/></g>)}
    <path d="M-130 180 L-148 205 L148 205 L130 180Z" fill={colors.coral} stroke={colors.brown} strokeWidth="5"/>
  </g>
);

export const DiwaliMarket: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const fade = interpolate(frame,[0,25, durationInFrames-25,durationInFrames],[0,1,1,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const titleOpacity = interpolate(frame,[15,45,125,155],[0,1,1,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const lanternY = interpolate(frame,[0,600],[0,-22]);
  return <AbsoluteFill style={{background:colors.night,opacity:fade,fontFamily:"Georgia, serif",overflow:"hidden"}}>
    <svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{position:"absolute",inset:0}}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#20394b"/><stop offset="100%" stopColor="#9a6558"/></linearGradient>
        <radialGradient id="moon"><stop offset="0%" stopColor="#fff2c7" stopOpacity=".9"/><stop offset="100%" stopColor="#fff2c7" stopOpacity="0"/></radialGradient>
      </defs>
      <rect width="1080" height="1920" fill="url(#sky)"/>
      <circle cx="825" cy="250" r="155" fill="url(#moon)"/><circle cx="825" cy="250" r="58" fill={colors.cream} opacity=".8"/>
      {Array.from({length:42},(_,i)=><Star key={i} x={(i*173+41)%1050+15} y={(i*97+50)%690+30} r={i%3===0?4:2} phase={i*9}/>)}
      <path d="M0 560 Q120 500 230 560 T470 550 T720 555 T1080 525 L1080 1150 L0 1150Z" fill="#314957" opacity=".75"/>
      <g transform={`translate(0 ${lanternY})`}>
        {[[145,180],[350,250],[610,155],[920,320],[770,470],[250,420]].map(([x,y],i)=><g key={i}><path d={`M${x} 0 L${x} ${y-28}`} stroke={colors.paper} strokeWidth="3" opacity=".7"/><path d={`M${x-23} ${y-28} Q${x} ${y-55} ${x+23} ${y-28} L${x+17} ${y+20} Q${x} ${y+38} ${x-17} ${y+20}Z`} fill={i%2?colors.coral:colors.gold} stroke={colors.paper} strokeWidth="3"/><path d={`M${x} ${y+25} L${x} ${y+45}`} stroke={colors.paper} strokeWidth="2"/></g>)}
      </g>
      <path d="M0 1030 Q540 930 1080 1035 L1080 1920 L0 1920Z" fill="#b77a5c"/>
      <path d="M0 1140 Q300 1080 550 1160 T1080 1125" fill="none" stroke="#e8b17b" strokeWidth="8" opacity=".6"/>
      <MarketStall x={240} y={1010} scale={1.05} accent="#c86e58"/>
      <MarketStall x={810} y={980} scale={1.12} accent="#d9a24e"/>
      <MarketStall x={530} y={1190} scale={.72} accent="#72998a"/>
      <g opacity=".96">
        {[[115,1510],[260,1600],[430,1505],[650,1605],[835,1510],[965,1630],[530,1745]].map(([x,y],i)=><Lamp key={i} x={x} y={y} scale={i===6?1.25:.9} delay={i*11}/>)}
      </g>
      <g fill={colors.brown} opacity=".9">
        <path d="M0 1810 Q180 1750 350 1815 T700 1800 T1080 1790 L1080 1920 L0 1920Z"/>
      </g>
      <g transform="translate(540 1420)">
        <ellipse cx="0" cy="150" rx="130" ry="24" fill="#f5c26a" opacity=".25"/>
        <path d="M-90 130 Q-125 25 -65 -25 L65 -25 Q125 25 90 130Z" fill="#d88a5e" stroke="#f5d8a0" strokeWidth="6"/>
        <path d="M-70 25 L70 25 M-82 70 L82 70 M-75 108 L75 108" stroke="#f6d69a" strokeWidth="7" opacity=".8"/>
        <path d="M0 -25 L0 -85 M-38 -65 L0 -85 L38 -65" fill="none" stroke="#f5d8a0" strokeWidth="6"/>
      </g>
      {Array.from({length:8},(_,i)=><g key={i} transform={`translate(${120+i*120} ${680+(i%2)*45})`} opacity=".85"><path d="M0 0 Q-20 28 -40 0 Q-20 -30 0 0 Q20 28 40 0 Q20 -30 0 0Z" fill={[colors.coral,colors.gold,colors.teal][i%3]}/><circle r="6" fill={colors.cream}/></g>)}
    </svg>
    <div style={{position:"absolute",top:120,left:55,right:55,textAlign:"center",opacity:titleOpacity,color:colors.cream,textShadow:"0 4px 20px #1a2730"}}>
      <div style={{fontSize:22,letterSpacing:8,textTransform:"uppercase",marginBottom:20}}>A watercolor dream</div>
      <div style={{fontSize:74,fontWeight:700,lineHeight:1.08}}>Diwali<br/>at the Market</div>
      <div style={{fontSize:25,marginTop:25,letterSpacing:2}}>Lights, colors & little joys</div>
    </div>
    <div style={{position:"absolute",bottom:80,left:40,right:40,textAlign:"center",fontSize:22,letterSpacing:4,color:"#fff0cf",opacity:interpolate(frame,[390,430,565,600],[0,.9,.9,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"})}}>HAPPY DIWALI</div>
  </AbsoluteFill>;
};
