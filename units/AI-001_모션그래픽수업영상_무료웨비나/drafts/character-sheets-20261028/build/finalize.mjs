import path from 'node:path';
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const source=path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_톤과움직임확장_21장_v13.pptx');
const out=path.join(R,'output/webinar-knowledge-only');await fs.mkdir(out,{recursive:true});
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const tables=[18,20];
const result=await finalizePresentation({workspaceDir:R,candidatePath:path.join(B,'candidate.pptx'),finalPath:path.join(out,'NotionTalk_모션그래픽_캐릭터시트적용_21장_v14.pptx'),pythonExecutable:'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...tables.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:21,requiredNativeTableOwnerSlides:tables,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'reference',families:['Pretendard'],referencePath:source,referenceSha256:createHash('sha256').update(await fs.readFile(source)).digest('hex')},verifyArtifactToolImport:true,receiptPath:path.join(B,'validation-v14.json')});
console.log('Finalized explanation deck:',result.finalPath);



