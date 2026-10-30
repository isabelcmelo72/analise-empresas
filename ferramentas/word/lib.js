const fs = require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,BorderStyle,AlignmentType,HeadingLevel,LevelFormat,Footer} = require('docx');
const NAVY='1F3A5F',GREY='5B6573',ZEBRA='F5F7FA',LINE='D0D5DD',GREEN='DDF0E3',AMBER='FFF1CC',RED='F8D9D6',BLUE='EAF1F8',FS=17,POS='0F6E56',NEG='A32D2D',NEU='444441';
function runs(t,o={}){return t.split('**').map((x,i)=>new TextRun({text:x,bold:(i%2===1)||o.b,italics:o.i,color:o.c,size:o.s||FS}))}
function P(t,o={}){return new Paragraph({children:runs(t,o),spacing:{before:o.before||0,after:o.after===undefined?40:o.after},shading:o.shade?{type:ShadingType.CLEAR,fill:o.shade,color:'auto'}:undefined})}
function B(t){return new Paragraph({children:runs(t),numbering:{reference:'bul',level:0},spacing:{after:15}})}
function H(t){return new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun({text:t})],spacing:{before:80,after:30}})}
const none={style:BorderStyle.NONE,size:0,color:'FFFFFF'},thin={style:BorderStyle.SINGLE,size:4,color:LINE};
function cell(spec,w,idx,head,size){const s=typeof spec==='string'?{c:spec}:spec;const fill=head?NAVY:(s.fill||(idx%2===0?ZEBRA:'FFFFFF'));
 return new TableCell({width:{size:w,type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill,color:'auto'},margins:{top:20,bottom:20,left:70,right:70},borders:{top:none,left:none,right:none,bottom:thin},children:[new Paragraph({spacing:{after:0},children:runs(s.c,{s:size,b:head||s.b,c:head?'FFFFFF':s.color})})]})}
function table(ws,rows,size=15){return new Table({width:{size:ws.reduce((a,b)=>a+b,0),type:WidthType.DXA},columnWidths:ws,rows:rows.map((r,i)=>new TableRow({tableHeader:i===0,cantSplit:true,children:r.map((c,j)=>cell(c,ws[j],i,i===0,size))}))})}
const pos=c=>({c,color:POS,b:true}),neg=c=>({c,color:NEG,b:true}),neu=c=>({c,color:NEU,b:true});
function report(d,OUT){
 const sealFill={G:GREEN,A:AMBER,R:RED}[d.seal.k];const kids=[];
 kids.push(new Paragraph({spacing:{after:0},children:[new TextRun({text:d.name,bold:true,size:32,color:NAVY})]}));
 kids.push(new Paragraph({spacing:{after:40},border:{bottom:{style:BorderStyle.SINGLE,size:8,color:NAVY,space:2}},children:[new TextRun({text:d.subtitle,size:17,color:GREY})]}));
 kids.push(new Paragraph({spacing:{after:40},children:[new TextRun({text:' Carteira Rui Jorge ',bold:true,size:15,color:'FFFFFF',shading:{type:ShadingType.CLEAR,fill:NAVY,color:'auto'}})]}));
 if(d.banner)kids.push(P(d.banner,{shade:'FDE8E6',s:15,after:40}));
 kids.push(P(`**${d.seal.label}** — ${d.seal.text}`,{shade:sealFill,after:30}));
 kids.push(H('Resultados do trimestre'));d.resultados.forEach(t=>kids.push(P(t)));
 kids.push(H('O negócio, em poucas palavras'));kids.push(P(d.negocio));
 kids.push(H('Moat (vantagem competitiva)'));d.moat.forEach(t=>kids.push(B(t)));
 kids.push(H('Indicadores-chave'));kids.push(table([2500,2500,4638],[['Indicador','Valor','Leitura'],...d.ind]));
 kids.push(P(d.verif.title,{before:40,b:true,c:NAVY,after:10,s:15}));d.verif.lines.forEach(t=>kids.push(P(t,{s:14,shade:BLUE,after:8})));
 kids.push(H('Clareza vs nossa leitura'));kids.push(table([1300,4169,4169],[['','Clareza','Nossa leitura'],...d.cmp]));
 kids.push(P(d.semdif,{s:15,before:30,after:20}));kids.push(P(d.entrada,{shade:NAVY,c:'FFFFFF',s:16,before:30,after:20}));
 kids.push(H('Valorização atual'));kids.push(table([3000,3000,3638],[['Referência','Valor','Fonte e data'],...d.val]));
 kids.push(H('Conclusão'));d.conclusao.forEach(t=>kids.push(P(t)));
 kids.push(H('Fontes e datas de consulta'));kids.push(table([3200,4538,1900],[['Fonte','Dados usados','Consulta'],...d.fontes],14));
 const doc=new Document({creator:'Claude',title:d.name,styles:{default:{document:{run:{font:'Calibri',size:FS}}},paragraphStyles:[{id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:20,bold:true,color:NAVY,font:'Calibri'},paragraph:{spacing:{before:80,after:30},outlineLevel:0}}]},
  numbering:{config:[{reference:'bul',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:300,hanging:200}}}}]}]},
  sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:500,bottom:500,left:1000,right:1000}}},footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:`${d.ticker} · Carteira Rui Jorge · análise de 30/10/2026 · Não é aconselhamento financeiro`,size:13,color:GREY})]})]})},children:kids}]});
 return Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT+d.file,b);console.log('ok',d.file)})}
module.exports={report,pos,neg,neu};
