import { useState } from 'react';
import { tokenAPI } from '../api/service';

export default function AdminLoginModal({ onSubmit, onClose }) {
    const [token, setToken] = useState('SECRET_TOKEN');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        setLoading(true);
        setError('');
        const res = await tokenAPI.verify(token);
        setLoading(false);
        if (res.success) {
            onSubmit(token);
        } else {
            setError('토큰이 일치하지 않습니다.');
        }
    };

    return (
        <div className="modal fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
            <div className="bg-white rounded-xl p-6 shadow-xl min-w-[300px]">
                <h2 className="font-bold text-lg mb-4">관리자 토큰 입력</h2>
                <input
                    className="border rounded px-2 py-1 w-full mb-2"
                    value={token}
                    onChange={e => setToken(e.target.value)}
                    placeholder="관리자 토큰 입력"
                    onKeyDown={e => { if (e.key === 'Enter') handleSubmit(); }}
                    disabled={loading}
                />
                {error && (
                    <div className="text-red-600 text-sm mb-2">{error}</div>
                )}
                <div className="flex gap-2 justify-end">
                    <button
                        className="bg-primary px-4 py-2 rounded text-black font-semibold"
                        onClick={handleSubmit}
                        disabled={loading}
                    >{loading ? '확인 중...' : '확인'}</button>
                    <button
                        className="bg-gray-300 px-4 py-2 rounded text-black font-semibold"
                        onClick={onClose}
                        disabled={loading}
                    >취소</button>
                </div>
            </div>
        </div>
    );
}

