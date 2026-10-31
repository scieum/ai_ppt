import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {Presentation,PresentationFile} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const manifest=JSON.parse(await fs.readFile(path.join(B,'manifest.json'),'utf8'));
const A=path.join(R,'assets/tool-logos/glass-color-v4');await fs.mkdir(A,{recursive:true});
const p=Presentation.create({slideSize:{width:1280,height:720}});
for (const m of manifest){await fs.copyFile(m.generated_path,path.join(R,m.asset));const s=p.slides.add();s.background.fill='#000000';s.images.add({blob:new Uint8Array(await fs.readFile(path.join(R,m.asset))),contentType:'image/png',fit:'contain',position:{left:247,top:333,width:153,height:153}});}
await fs.copyFile(path.join(R,'assets/tool-logos/glass-v3/codex-front.png'),path.join(A,'codex-front.png'));
await fs.writeFile(path.join(A,'manifest.json'),JSON.stringify(manifest,null,2));
await fs.writeFile(path.join(A,'README.md'),'# 로고 색 복원\n\n클로드의 코랄색과 힉스필드의 라임색을 복원했습니다. 코덱스의 흰색과 유리 타일은 유지합니다. 주황 테두리·모서리 장식은 복원하지 않습니다.\n\nbuilt-in ImageGen을 사용했습니다. 생성 프롬프트와 원본 경로는 manifest.json에 있습니다. 세 PNG는 이 폴더에 저장했습니다.\n');
await(await PresentationFile.exportPptx(p)).save(path.join(B,'colored-assets.pptx'));
console.log('Saved two colored glass assets; retained white Codex.');
