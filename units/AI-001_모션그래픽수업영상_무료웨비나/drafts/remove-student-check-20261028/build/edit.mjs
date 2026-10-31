import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness/output/webinar-flipbook/NotionTalk_플립북설명추가_22장_v1.pptx'));
const s=p.slides.items[19];
if(!s.shapes.items.some(x=>String(x.text).includes('학생이 따라올 수 있는 영상인가요?')))throw Error('Wrong deletion target');
s.delete();
await(await PresentationFile.exportPptx(p)).save('C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness/units/AI-001_모션그래픽수업영상_무료웨비나/drafts/remove-student-check-20261028/build/edited-roundtrip.pptx');
console.log('Deleted the identified student-review slide; 21 slides remain.');
