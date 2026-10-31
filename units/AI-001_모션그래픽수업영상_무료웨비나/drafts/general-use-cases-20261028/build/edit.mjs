import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v3.pptx'))),s=p.slides.items[5];
const values={'dev-format-head-2':'주로 쓰이는 상황','dev-format-0-2':'광고 문구·행사 안내','dev-format-1-2':'통계·성과·과정 설명','dev-format-2-2':'제품 기능·서비스 사용법','dev-format-3-2':'브랜드 소개·영상 오프닝','dev-format-4-2':'상황 재현·스토리 설명'};
for(const[n,v]of Object.entries(values)){const sh=s.shapes.items.find(x=>x.name===n);if(!sh)throw Error(n);sh.text.replace(String(sh.text),v);}
s.speakerNotes.text='움직이는 글자를 중심으로 하면 키네틱 타이포그래피입니다. 광고 문구나 행사 안내에서 자주 볼 수 있습니다. 인포그래픽은 통계·성과·과정을 설명하고, UI·서비스 소개는 제품 기능과 사용법을 보여 줍니다. 로고·타이틀은 브랜드 소개와 영상 오프닝, 일러스트·캐릭터는 상황 재현과 스토리 설명에 활용할 수 있습니다. 서로 겹칠 수 있는 실용적 분류이며 한 영상에서 함께 사용할 수 있습니다. 오늘 세 사례는 같은 기준의 세 장르가 아닙니다. 타이포그래피는 표현 형식, URL은 입력 방법, 과학사는 설명 주제입니다. 참가자가 평소 본 영상에서 어떤 요소가 움직였는지 떠올리게 합니다.\n근거: https://www.autodesk.com/uk/solutions/motion-graphics\nhttps://support.apple.com/guide/motion/intro-to-animated-text-motn17692a95/6.3/mac/15.6\n활용 상황은 이번 웨비나를 위한 자체 예시입니다.';
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Updated slide 6 to general use cases.');
