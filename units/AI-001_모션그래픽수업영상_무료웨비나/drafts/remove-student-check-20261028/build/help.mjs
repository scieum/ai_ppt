import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness/output/webinar-flipbook/NotionTalk_플립북설명추가_22장_v1.pptx'));
console.log((await p.help('*',{search:'slide.*delete|slides.*delete|slide.*remove',include:['index','examples'],maxChars:2200})).ndjson);
