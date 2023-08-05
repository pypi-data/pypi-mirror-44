(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d2371be"],{fa5b:function(e,n,t){"use strict";t.r(n);var r,i,o,a,u,s,c,d,f,l,g,h,p,m,v,b=12e4,_=function(){function e(e){var n=this;this._defaults=e,this._worker=null,this._idleCheckInterval=setInterval(function(){return n._checkIfIdle()},3e4),this._lastUsedTime=0,this._configChangeListener=this._defaults.onDidChange(function(){return n._stopWorker()})}return e.prototype._stopWorker=function(){this._worker&&(this._worker.dispose(),this._worker=null),this._client=null},e.prototype.dispose=function(){clearInterval(this._idleCheckInterval),this._configChangeListener.dispose(),this._stopWorker()},e.prototype._checkIfIdle=function(){if(this._worker){var e=Date.now()-this._lastUsedTime;e>b&&this._stopWorker()}},e.prototype._getClient=function(){return this._lastUsedTime=Date.now(),this._client||(this._worker=monaco.editor.createWebWorker({moduleId:"vs/language/html/htmlWorker",createData:{languageSettings:this._defaults.options,languageId:this._defaults.languageId},label:this._defaults.languageId}),this._client=this._worker.getProxy()),this._client},e.prototype.getLanguageServiceWorker=function(){for(var e,n=this,t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];return this._getClient().then(function(n){e=n}).then(function(e){return n._worker.withSyncedResources(t)}).then(function(n){return e})},e}();(function(e){function n(e,n){return{line:e,character:n}}function t(e){var n=e;return B.objectLiteral(n)&&B.number(n.line)&&B.number(n.character)}e.create=n,e.is=t})(r||(r={})),function(e){function n(e,n,t,i){if(B.number(e)&&B.number(n)&&B.number(t)&&B.number(i))return{start:r.create(e,n),end:r.create(t,i)};if(r.is(e)&&r.is(n))return{start:e,end:n};throw new Error("Range#create called with invalid arguments["+e+", "+n+", "+t+", "+i+"]")}function t(e){var n=e;return B.objectLiteral(n)&&r.is(n.start)&&r.is(n.end)}e.create=n,e.is=t}(i||(i={})),function(e){function n(e,n){return{uri:e,range:n}}function t(e){var n=e;return B.defined(n)&&i.is(n.range)&&(B.string(n.uri)||B.undefined(n.uri))}e.create=n,e.is=t}(o||(o={})),function(e){function n(e,n,t,r){return{red:e,green:n,blue:t,alpha:r}}function t(e){var n=e;return B.number(n.red)&&B.number(n.green)&&B.number(n.blue)&&B.number(n.alpha)}e.create=n,e.is=t}(a||(a={})),function(e){function n(e,n){return{range:e,color:n}}function t(e){var n=e;return i.is(n.range)&&a.is(n.color)}e.create=n,e.is=t}(u||(u={})),function(e){function n(e,n,t){return{label:e,textEdit:n,additionalTextEdits:t}}function t(e){var n=e;return B.string(n.label)&&(B.undefined(n.textEdit)||p.is(n))&&(B.undefined(n.additionalTextEdits)||B.typedArray(n.additionalTextEdits,p.is))}e.create=n,e.is=t}(s||(s={})),function(e){e["Comment"]="comment",e["Imports"]="imports",e["Region"]="region"}(c||(c={})),function(e){function n(e,n,t,r,i){var o={startLine:e,endLine:n};return B.defined(t)&&(o.startCharacter=t),B.defined(r)&&(o.endCharacter=r),B.defined(i)&&(o.kind=i),o}function t(e){var n=e;return B.number(n.startLine)&&B.number(n.startLine)&&(B.undefined(n.startCharacter)||B.number(n.startCharacter))&&(B.undefined(n.endCharacter)||B.number(n.endCharacter))&&(B.undefined(n.kind)||B.string(n.kind))}e.create=n,e.is=t}(d||(d={})),function(e){function n(e,n){return{location:e,message:n}}function t(e){var n=e;return B.defined(n)&&o.is(n.location)&&B.string(n.message)}e.create=n,e.is=t}(f||(f={})),function(e){e.Error=1,e.Warning=2,e.Information=3,e.Hint=4}(l||(l={})),function(e){function n(e,n,t,r,i,o){var a={range:e,message:n};return B.defined(t)&&(a.severity=t),B.defined(r)&&(a.code=r),B.defined(i)&&(a.source=i),B.defined(o)&&(a.relatedInformation=o),a}function t(e){var n=e;return B.defined(n)&&i.is(n.range)&&B.string(n.message)&&(B.number(n.severity)||B.undefined(n.severity))&&(B.number(n.code)||B.string(n.code)||B.undefined(n.code))&&(B.string(n.source)||B.undefined(n.source))&&(B.undefined(n.relatedInformation)||B.typedArray(n.relatedInformation,f.is))}e.create=n,e.is=t}(g||(g={})),function(e){function n(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={title:e,command:n};return B.defined(t)&&t.length>0&&(i.arguments=t),i}function t(e){var n=e;return B.defined(n)&&B.string(n.title)&&B.string(n.command)}e.create=n,e.is=t}(h||(h={})),function(e){function n(e,n){return{range:e,newText:n}}function t(e,n){return{range:{start:e,end:e},newText:n}}function r(e){return{range:e,newText:""}}function o(e){var n=e;return B.objectLiteral(n)&&B.string(n.newText)&&i.is(n.range)}e.replace=n,e.insert=t,e.del=r,e.is=o}(p||(p={})),function(e){function n(e,n){return{textDocument:e,edits:n}}function t(e){var n=e;return B.defined(n)&&w.is(n.textDocument)&&Array.isArray(n.edits)}e.create=n,e.is=t}(m||(m={})),function(e){function n(e){var n=e;return n&&(void 0!==n.changes||void 0!==n.documentChanges)&&(void 0===n.documentChanges||B.typedArray(n.documentChanges,m.is))}e.is=n}(v||(v={}));var y,w,k,x,C,E,I,T,S,M,R,P,A,F,L,O,j,D=function(){function e(e){this.edits=e}return e.prototype.insert=function(e,n){this.edits.push(p.insert(e,n))},e.prototype.replace=function(e,n){this.edits.push(p.replace(e,n))},e.prototype.delete=function(e){this.edits.push(p.del(e))},e.prototype.add=function(e){this.edits.push(e)},e.prototype.all=function(){return this.edits},e.prototype.clear=function(){this.edits.splice(0,this.edits.length)},e}();(function(){function e(e){var n=this;this._textEditChanges=Object.create(null),e&&(this._workspaceEdit=e,e.documentChanges?e.documentChanges.forEach(function(e){var t=new D(e.edits);n._textEditChanges[e.textDocument.uri]=t}):e.changes&&Object.keys(e.changes).forEach(function(t){var r=new D(e.changes[t]);n._textEditChanges[t]=r}))}Object.defineProperty(e.prototype,"edit",{get:function(){return this._workspaceEdit},enumerable:!0,configurable:!0}),e.prototype.getTextEditChange=function(e){if(w.is(e)){if(this._workspaceEdit||(this._workspaceEdit={documentChanges:[]}),!this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for versioned document changes.");var n=e,t=this._textEditChanges[n.uri];if(!t){var r=[],i={textDocument:n,edits:r};this._workspaceEdit.documentChanges.push(i),t=new D(r),this._textEditChanges[n.uri]=t}return t}if(this._workspaceEdit||(this._workspaceEdit={changes:Object.create(null)}),!this._workspaceEdit.changes)throw new Error("Workspace edit is not configured for normal text edit changes.");t=this._textEditChanges[e];if(!t){r=[];this._workspaceEdit.changes[e]=r,t=new D(r),this._textEditChanges[e]=t}return t}})();(function(e){function n(e){return{uri:e}}function t(e){var n=e;return B.defined(n)&&B.string(n.uri)}e.create=n,e.is=t})(y||(y={})),function(e){function n(e,n){return{uri:e,version:n}}function t(e){var n=e;return B.defined(n)&&B.string(n.uri)&&B.number(n.version)}e.create=n,e.is=t}(w||(w={})),function(e){function n(e,n,t,r){return{uri:e,languageId:n,version:t,text:r}}function t(e){var n=e;return B.defined(n)&&B.string(n.uri)&&B.string(n.languageId)&&B.number(n.version)&&B.string(n.text)}e.create=n,e.is=t}(k||(k={})),function(e){e.PlainText="plaintext",e.Markdown="markdown"}(x||(x={})),function(e){function n(n){var t=n;return t===e.PlainText||t===e.Markdown}e.is=n}(x||(x={})),function(e){function n(e){var n=e;return B.objectLiteral(e)&&x.is(n.kind)&&B.string(n.value)}e.is=n}(C||(C={})),function(e){e.Text=1,e.Method=2,e.Function=3,e.Constructor=4,e.Field=5,e.Variable=6,e.Class=7,e.Interface=8,e.Module=9,e.Property=10,e.Unit=11,e.Value=12,e.Enum=13,e.Keyword=14,e.Snippet=15,e.Color=16,e.File=17,e.Reference=18,e.Folder=19,e.EnumMember=20,e.Constant=21,e.Struct=22,e.Event=23,e.Operator=24,e.TypeParameter=25}(E||(E={})),function(e){e.PlainText=1,e.Snippet=2}(I||(I={})),function(e){function n(e){return{label:e}}e.create=n}(T||(T={})),function(e){function n(e,n){return{items:e||[],isIncomplete:!!n}}e.create=n}(S||(S={})),function(e){function n(e){return e.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}function t(e){var n=e;return B.string(n)||B.objectLiteral(n)&&B.string(n.language)&&B.string(n.value)}e.fromPlainText=n,e.is=t}(M||(M={})),function(e){function n(e){var n=e;return B.objectLiteral(n)&&(C.is(n.contents)||M.is(n.contents)||B.typedArray(n.contents,M.is))&&(void 0===e.range||i.is(e.range))}e.is=n}(R||(R={})),function(e){function n(e,n){return n?{label:e,documentation:n}:{label:e}}e.create=n}(P||(P={})),function(e){function n(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={label:e};return B.defined(n)&&(i.documentation=n),B.defined(t)?i.parameters=t:i.parameters=[],i}e.create=n}(A||(A={})),function(e){e.Text=1,e.Read=2,e.Write=3}(F||(F={})),function(e){function n(e,n){var t={range:e};return B.number(n)&&(t.kind=n),t}e.create=n}(L||(L={})),function(e){e.File=1,e.Module=2,e.Namespace=3,e.Package=4,e.Class=5,e.Method=6,e.Property=7,e.Field=8,e.Constructor=9,e.Enum=10,e.Interface=11,e.Function=12,e.Variable=13,e.Constant=14,e.String=15,e.Number=16,e.Boolean=17,e.Array=18,e.Object=19,e.Key=20,e.Null=21,e.EnumMember=22,e.Struct=23,e.Event=24,e.Operator=25,e.TypeParameter=26}(O||(O={})),function(e){function n(e,n,t,r,i){var o={name:e,kind:n,location:{uri:r,range:t}};return i&&(o.containerName=i),o}e.create=n}(j||(j={}));var W,V,K,N,H,U=function(){function e(){}return e}();(function(e){function n(e,n,t,r,i,o){var a={name:e,detail:n,kind:t,range:r,selectionRange:i};return void 0!==o&&(a.children=o),a}function t(e){var n=e;return n&&B.string(n.name)&&B.string(n.detail)&&B.number(n.kind)&&i.is(n.range)&&i.is(n.selectionRange)&&(void 0===n.deprecated||B.boolean(n.deprecated))&&(void 0===n.children||Array.isArray(n.children))}e.create=n,e.is=t})(U||(U={})),function(e){e.QuickFix="quickfix",e.Refactor="refactor",e.RefactorExtract="refactor.extract",e.RefactorInline="refactor.inline",e.RefactorRewrite="refactor.rewrite",e.Source="source",e.SourceOrganizeImports="source.organizeImports"}(W||(W={})),function(e){function n(e,n){var t={diagnostics:e};return void 0!==n&&null!==n&&(t.only=n),t}function t(e){var n=e;return B.defined(n)&&B.typedArray(n.diagnostics,g.is)&&(void 0===n.only||B.typedArray(n.only,B.string))}e.create=n,e.is=t}(V||(V={})),function(e){function n(e,n,t){var r={title:e};return h.is(n)?r.command=n:r.edit=n,void 0!==t&&(r.kind=t),r}function t(e){var n=e;return n&&B.string(n.title)&&(void 0===n.diagnostics||B.typedArray(n.diagnostics,g.is))&&(void 0===n.kind||B.string(n.kind))&&(void 0!==n.edit||void 0!==n.command)&&(void 0===n.command||h.is(n.command))&&(void 0===n.edit||v.is(n.edit))}e.create=n,e.is=t}(K||(K={})),function(e){function n(e,n){var t={range:e};return B.defined(n)&&(t.data=n),t}function t(e){var n=e;return B.defined(n)&&i.is(n.range)&&(B.undefined(n.command)||h.is(n.command))}e.create=n,e.is=t}(N||(N={})),function(e){function n(e,n){return{tabSize:e,insertSpaces:n}}function t(e){var n=e;return B.defined(n)&&B.number(n.tabSize)&&B.boolean(n.insertSpaces)}e.create=n,e.is=t}(H||(H={}));var z=function(){function e(){}return e}();(function(e){function n(e,n,t){return{range:e,target:n,data:t}}function t(e){var n=e;return B.defined(n)&&i.is(n.range)&&(B.undefined(n.target)||B.string(n.target))}e.create=n,e.is=t})(z||(z={}));var J,q;(function(e){function n(e,n,t,r){return new Q(e,n,t,r)}function t(e){var n=e;return!!(B.defined(n)&&B.string(n.uri)&&(B.undefined(n.languageId)||B.string(n.languageId))&&B.number(n.lineCount)&&B.func(n.getText)&&B.func(n.positionAt)&&B.func(n.offsetAt))}function r(e,n){for(var t=e.getText(),r=i(n,function(e,n){var t=e.range.start.line-n.range.start.line;return 0===t?e.range.start.character-n.range.start.character:t}),o=t.length,a=r.length-1;a>=0;a--){var u=r[a],s=e.offsetAt(u.range.start),c=e.offsetAt(u.range.end);if(!(c<=o))throw new Error("Ovelapping edit");t=t.substring(0,s)+u.newText+t.substring(c,t.length),o=s}return t}function i(e,n){if(e.length<=1)return e;var t=e.length/2|0,r=e.slice(0,t),o=e.slice(t);i(r,n),i(o,n);var a=0,u=0,s=0;while(a<r.length&&u<o.length){var c=n(r[a],o[u]);e[s++]=c<=0?r[a++]:o[u++]}while(a<r.length)e[s++]=r[a++];while(u<o.length)e[s++]=o[u++];return e}e.create=n,e.is=t,e.applyEdits=r})(J||(J={})),function(e){e.Manual=1,e.AfterDelay=2,e.FocusOut=3}(q||(q={}));var B,Q=function(){function e(e,n,t,r){this._uri=e,this._languageId=n,this._version=t,this._content=r,this._lineOffsets=null}return Object.defineProperty(e.prototype,"uri",{get:function(){return this._uri},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"languageId",{get:function(){return this._languageId},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"version",{get:function(){return this._version},enumerable:!0,configurable:!0}),e.prototype.getText=function(e){if(e){var n=this.offsetAt(e.start),t=this.offsetAt(e.end);return this._content.substring(n,t)}return this._content},e.prototype.update=function(e,n){this._content=e.text,this._version=n,this._lineOffsets=null},e.prototype.getLineOffsets=function(){if(null===this._lineOffsets){for(var e=[],n=this._content,t=!0,r=0;r<n.length;r++){t&&(e.push(r),t=!1);var i=n.charAt(r);t="\r"===i||"\n"===i,"\r"===i&&r+1<n.length&&"\n"===n.charAt(r+1)&&r++}t&&n.length>0&&e.push(n.length),this._lineOffsets=e}return this._lineOffsets},e.prototype.positionAt=function(e){e=Math.max(Math.min(e,this._content.length),0);var n=this.getLineOffsets(),t=0,i=n.length;if(0===i)return r.create(0,e);while(t<i){var o=Math.floor((t+i)/2);n[o]>e?i=o:t=o+1}var a=t-1;return r.create(a,e-n[a])},e.prototype.offsetAt=function(e){var n=this.getLineOffsets();if(e.line>=n.length)return this._content.length;if(e.line<0)return 0;var t=n[e.line],r=e.line+1<n.length?n[e.line+1]:this._content.length;return Math.max(Math.min(t+e.character,r),t)},Object.defineProperty(e.prototype,"lineCount",{get:function(){return this.getLineOffsets().length},enumerable:!0,configurable:!0}),e}();(function(e){var n=Object.prototype.toString;function t(e){return"undefined"!==typeof e}function r(e){return"undefined"===typeof e}function i(e){return!0===e||!1===e}function o(e){return"[object String]"===n.call(e)}function a(e){return"[object Number]"===n.call(e)}function u(e){return"[object Function]"===n.call(e)}function s(e){return null!==e&&"object"===typeof e}function c(e,n){return Array.isArray(e)&&e.every(n)}e.defined=t,e.undefined=r,e.boolean=i,e.string=o,e.number=a,e.func=u,e.objectLiteral=s,e.typedArray=c})(B||(B={}));var $=monaco.Range,G=function(){function e(e,n,t){var r=this;this._languageId=e,this._worker=n,this._disposables=[],this._listener=Object.create(null);var i=function(e){var n,t=e.getModeId();t===r._languageId&&(r._listener[e.uri.toString()]=e.onDidChangeContent(function(){clearTimeout(n),n=setTimeout(function(){return r._doValidate(e.uri,t)},500)}),r._doValidate(e.uri,t))},o=function(e){monaco.editor.setModelMarkers(e,r._languageId,[]);var n=e.uri.toString(),t=r._listener[n];t&&(t.dispose(),delete r._listener[n])};this._disposables.push(monaco.editor.onDidCreateModel(i)),this._disposables.push(monaco.editor.onWillDisposeModel(function(e){o(e)})),this._disposables.push(monaco.editor.onDidChangeModelLanguage(function(e){o(e.model),i(e.model)})),this._disposables.push(t.onDidChange(function(e){monaco.editor.getModels().forEach(function(e){e.getModeId()===r._languageId&&(o(e),i(e))})})),this._disposables.push({dispose:function(){for(var e in r._listener)r._listener[e].dispose()}}),monaco.editor.getModels().forEach(i)}return e.prototype.dispose=function(){this._disposables.forEach(function(e){return e&&e.dispose()}),this._disposables=[]},e.prototype._doValidate=function(e,n){this._worker(e).then(function(t){return t.doValidation(e.toString()).then(function(t){var r=t.map(function(n){return Y(e,n)});monaco.editor.setModelMarkers(monaco.editor.getModel(e),n,r)})}).then(void 0,function(e){console.error(e)})},e}();function X(e){switch(e){case l.Error:return monaco.MarkerSeverity.Error;case l.Warning:return monaco.MarkerSeverity.Warning;case l.Information:return monaco.MarkerSeverity.Info;case l.Hint:return monaco.MarkerSeverity.Hint;default:return monaco.MarkerSeverity.Info}}function Y(e,n){var t="number"===typeof n.code?String(n.code):n.code;return{severity:X(n.severity),startLineNumber:n.range.start.line+1,startColumn:n.range.start.character+1,endLineNumber:n.range.end.line+1,endColumn:n.range.end.character+1,message:n.message,code:t,source:n.source}}function Z(e){if(e)return{character:e.column-1,line:e.lineNumber-1}}function ee(e){if(e)return{start:Z(e.getStartPosition()),end:Z(e.getEndPosition())}}function ne(e){if(e)return new $(e.start.line+1,e.start.character+1,e.end.line+1,e.end.character+1)}function te(e){var n=monaco.languages.CompletionItemKind;switch(e){case E.Text:return n.Text;case E.Method:return n.Method;case E.Function:return n.Function;case E.Constructor:return n.Constructor;case E.Field:return n.Field;case E.Variable:return n.Variable;case E.Class:return n.Class;case E.Interface:return n.Interface;case E.Module:return n.Module;case E.Property:return n.Property;case E.Unit:return n.Unit;case E.Value:return n.Value;case E.Enum:return n.Enum;case E.Keyword:return n.Keyword;case E.Snippet:return n.Snippet;case E.Color:return n.Color;case E.File:return n.File;case E.Reference:return n.Reference}return n.Property}function re(e){if(e)return{range:ne(e.range),text:e.newText}}var ie=function(){function e(e){this._worker=e}return Object.defineProperty(e.prototype,"triggerCharacters",{get:function(){return[".",":","<",'"',"=","/"]},enumerable:!0,configurable:!0}),e.prototype.provideCompletionItems=function(e,n,t,r){e.getWordUntilPosition(n);var i=e.uri;return this._worker(i).then(function(e){return e.doComplete(i.toString(),Z(n))}).then(function(e){if(e){var n=e.items.map(function(e){var n={label:e.label,insertText:e.insertText||e.label,sortText:e.sortText,filterText:e.filterText,documentation:e.documentation,detail:e.detail,kind:te(e.kind)};return e.textEdit&&(n.range=ne(e.textEdit.range),n.insertText=e.textEdit.newText),e.additionalTextEdits&&(n.additionalTextEdits=e.additionalTextEdits.map(re)),e.insertTextFormat===I.Snippet&&(n.insertTextRules=monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet),n});return{isIncomplete:e.isIncomplete,suggestions:n}}})},e}();function oe(e){var n=monaco.languages.DocumentHighlightKind;switch(e){case F.Read:return n.Read;case F.Write:return n.Write;case F.Text:return n.Text}return n.Text}var ae=function(){function e(e){this._worker=e}return e.prototype.provideDocumentHighlights=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.findDocumentHighlights(r.toString(),Z(n))}).then(function(e){if(e)return e.map(function(e){return{range:ne(e.range),kind:oe(e.kind)}})})},e}(),ue=function(){function e(e){this._worker=e}return e.prototype.provideLinks=function(e,n){var t=e.uri;return this._worker(t).then(function(e){return e.findDocumentLinks(t.toString())}).then(function(e){if(e)return e.map(function(e){return{range:ne(e.range),url:e.target}})})},e}();function se(e){return{tabSize:e.tabSize,insertSpaces:e.insertSpaces}}var ce=function(){function e(e){this._worker=e}return e.prototype.provideDocumentFormattingEdits=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.format(r.toString(),null,se(n)).then(function(e){if(e&&0!==e.length)return e.map(re)})})},e}(),de=function(){function e(e){this._worker=e}return e.prototype.provideDocumentRangeFormattingEdits=function(e,n,t,r){var i=e.uri;return this._worker(i).then(function(e){return e.format(i.toString(),ee(n),se(t)).then(function(e){if(e&&0!==e.length)return e.map(re)})})},e}(),fe=function(){function e(e){this._worker=e}return e.prototype.provideFoldingRanges=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.provideFoldingRanges(r.toString(),n)}).then(function(e){if(e)return e.map(function(e){var n={start:e.startLine+1,end:e.endLine+1};return"undefined"!==typeof e.kind&&(n.kind=le(e.kind)),n})})},e}();function le(e){switch(e){case c.Comment:return monaco.languages.FoldingRangeKind.Comment;case c.Imports:return monaco.languages.FoldingRangeKind.Imports;case c.Region:return monaco.languages.FoldingRangeKind.Region}}function ge(e){var n=new _(e),t=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return n.getLanguageServiceWorker.apply(n,e)},r=e.languageId;monaco.languages.registerCompletionItemProvider(r,new ie(t)),monaco.languages.registerDocumentHighlightProvider(r,new ae(t)),monaco.languages.registerLinkProvider(r,new ue(t)),monaco.languages.registerFoldingRangeProvider(r,new fe(t)),"html"===r&&(monaco.languages.registerDocumentFormattingEditProvider(r,new ce(t)),monaco.languages.registerDocumentRangeFormattingEditProvider(r,new de(t)),new G(r,t,e))}t.d(n,"setupMode",function(){return ge})}}]);