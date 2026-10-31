import path from'node:path';import fs from'node:fs/promises';import{createHash}from'node:crypto';import{fileURLToPath,pathToFileURL}from'node:url';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..'),skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const source=path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_캐릭터시트적용_21장_v14.pptx');const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
for(const job of [
 {key:'library',count:20,tables:[6],final:path.join(R,'assets/layout-library-20261028/NotionTalk_상황별레이아웃_20종_v2.pptx')},
 
]){
 const result=await finalizePresentation({workspaceDir:R,candidatePath:path.join(B,job.key+'-candidate.pptx'),finalPath:job.final,pythonExecutable:'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...job.tables.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:job.count,requiredNativeTableOwnerSlides:job.tables,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'reference',families:['Pretendard'],referencePath:source,referenceSha256:createHash('sha256').update(await fs.readFile(source)).digest('hex')},verifyArtifactToolImport:true,receiptPath:path.join(B,job.key+'-validation-v2.json')});console.log(job.key+': '+result.finalPath);
}

