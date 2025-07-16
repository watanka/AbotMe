import React, { useRef, useState } from "react";
import { resumeAPI } from "../api/service";

function UploadField({ label, type = "text", value, onChange, placeholder, required, disabled }) {
  return (
    <label className="block mb-6">
      <span className="block mb-1 text-base font-extrabold text-primary-900">{label}</span>
      <input
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        placeholder={placeholder}
        className="w-full rounded-xl border-2 border-primary-300 px-5 py-4 text-lg font-bold bg-primary/5 text-primary-900 placeholder-primary-400 focus:border-primary-400 focus:ring-2 focus:ring-primary-300 outline-none transition disabled:opacity-50 disabled:bg-primary/20"
        aria-label={label}
      />
    </label>
  );
}

function Dropzone({ file, onFileChange, disabled }) {
  const inputRef = useRef();
  const [dragActive, setDragActive] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileChange(e.dataTransfer.files[0]);
    }
  };
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragActive(true);
  };
  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragActive(false);
  };
  const handleClick = () => {
    if (!disabled) inputRef.current?.click();
  };
  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileChange(e.target.files[0]);
    }
  };

  return (
    <div
      className={`w-full flex flex-col items-center justify-center border-4 border-primary-700 border-dashed rounded-3xl p-10 mb-8 transition cursor-pointer select-none ${dragActive ? "bg-primary/20" : "bg-primary/10 hover:bg-primary/20"} ${disabled ? "opacity-60 cursor-not-allowed" : ""}`}
      onClick={handleClick}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      tabIndex={0}
      role="button"
      aria-disabled={disabled}
      style={{ outline: "none" }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={handleChange}
        disabled={disabled}
        tabIndex={-1}
      />
      {file ? (
        <div className="flex items-center gap-3 text-primary-900 font-extrabold text-lg">
          <span className="truncate max-w-[260px]">{file.name}</span>
        </div>
      ) : (
        <>
          <span className="material-symbols-rounded text-6xl text-primary-700 mb-3">upload_file</span>
          <span className="text-primary-900 font-extrabold text-xl mb-2">PDF 파일을 드래그하거나 클릭하여 업로드</span>
          <span className="text-base text-primary-400">(최대 10MB, PDF만 가능)</span>
        </>
      )}
    </div>
  );
}

function SuccessResult({ editToken, publicUrl }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => {
    if (!editToken) return;
    try {
      await navigator.clipboard.writeText(editToken);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) { /* 복사 실패 무시 */ }
  };
  return (
    <div className="bg-green-100/90 border-2 border-green-400 text-green-900 rounded-2xl p-6 text-center mb-6 relative font-bold">
      <div className="font-semibold mb-2">업로드 성공!</div>
      <div className="flex items-center justify-center gap-2 text-sm">
        <span>edit_token:</span>
        <span className="font-mono break-all bg-white border border-green-200 rounded px-2 py-0.5 select-all">{editToken}</span>
        <button
          className="ml-3 px-4 py-2 rounded-xl bg-green-700 text-white text-base font-bold shadow hover:bg-green-800 active:bg-green-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-300 transition"
          onClick={handleCopy}
          aria-label="edit_token 복사"
          type="button"
        >
          복사
        </button>
      </div>
      <div className="text-sm mt-1">공개 URL: <a href={publicUrl} className="text-primary underline break-all" target="_blank" rel="noopener noreferrer">{publicUrl}</a></div>
      {copied && (
        <div className="fixed left-1/2 bottom-10 -translate-x-1/2 bg-green-700 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-fade-in">
          복사되었습니다!
        </div>
      )}
    </div>
  );
}



export default function ResumeUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [name, setName] = useState("eunsung"); // TODO: 임시 설정
  const [email, setEmail] = useState("eunsung@naver.com"); // TODO: 임시 설정
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(null); // { edit_token, public_url }

  const isValid = file && name.trim() && email.trim() && !loading;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(null);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("name", name);
      formData.append("email", email);
      const data = await resumeAPI.upload(formData);
      setSuccess(data);
      if (onUploadSuccess) onUploadSuccess(data);
    } catch (err) {
      setError(err.message || "알 수 없는 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="w-full max-w-lg mx-auto p-8 bg-white rounded-lg shadow mt-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">이력서 업로드</h2>
      {success ? (
        <SuccessResult pdf_url={success.pdf_url} />
      ) : (
        <form onSubmit={handleSubmit} autoComplete="off">
          <Dropzone file={file} onFileChange={setFile} disabled={loading} />
          <UploadField label="이름" value={name} onChange={e => setName(e.target.value)} placeholder="홍길동" required disabled={loading} />
          <UploadField label="이메일" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="your@email.com" required disabled={loading} />
          {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
          <button
            type="submit"
            className="w-full mt-8 py-4 rounded-3xl bg-primary-700 text-black font-extrabold text-2xl shadow-2xl border-0 hover:bg-primary-800 active:bg-primary-900 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-primary-300 transition-colors duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
            disabled={!isValid}
            aria-label="이력서 업로드"
          >
            {loading ? "업로드 중..." : "업로드"}
          </button>
        </form>
      )}
    </section>
  );
}
