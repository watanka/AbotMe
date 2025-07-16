import { useState } from 'react';

export default function AdminLoginModal({ onSubmit, onClose }) {
    const [token, setToken] = useState('VALID_TOKEN'); // TODO: 데모를 위해 미리 값 채워놓음
    return (
        <div className="modal fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
            <div className="bg-white rounded-xl p-6 shadow-xl min-w-[300px]">
                <h2 className="font-bold text-lg mb-4">관리자 토큰 입력</h2>
                <form
                    onSubmit={e => {
                        e.preventDefault();
                        onSubmit(token);
                    }}
                >
                    <input
                        className="border rounded px-2 py-1 w-full mb-4"
                        value={token}
                        onChange={e => setToken(e.target.value)}
                        placeholder="관리자 토큰 입력"
                        autoFocus
                    />
                    <div className="flex gap-2 justify-end">
                        <button
                            type="submit"
                            className="bg-primary px-4 py-2 rounded text-black font-semibold"
                        >확인</button>
                        <button
                            type="button"
                            className="bg-gray-300 px-4 py-2 rounded text-black font-semibold"
                            onClick={onClose}
                        >취소</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
