import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

interface NewsletterSettingsProps {
    projectId: string;
}

interface NewsletterPreferences {
    projectId: string;
    enabled: boolean;
    cadence: string;
    dayOfWeek: string;
}

export function NewsletterSettings({ projectId }: NewsletterSettingsProps) {
    const [enabled, setEnabled] = useState(false);
    const [cadence, setCadence] = useState('Weekly');
    const [dayOfWeek, setDayOfWeek] = useState('Monday');
    const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

    const mutation = useMutation({
        mutationFn: async (prefs: NewsletterPreferences) => {
            const response = await fetch('/api/subscribe_newsletter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(prefs),
            });

            if (!response.ok) {
                throw new Error('Failed to save preferences');
            }
            return response.json();
        },
        onSuccess: () => {
            setStatusMessage({ type: 'success', text: 'Preferences saved successfully!' });
            setTimeout(() => setStatusMessage(null), 3000);
        },
        onError: () => {
            setStatusMessage({ type: 'error', text: 'Failed to save preferences.' });
            setTimeout(() => setStatusMessage(null), 3000);
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        mutation.mutate({ projectId, enabled, cadence, dayOfWeek });
    };

    return (
        <div className="glass p-6 rounded-xl h-fit sticky top-6">
            <h3 className="text-xl font-semibold mb-4 text-[#222]">Newsletter Settings</h3>
            <p className="text-sm text-gray-600 mb-6">
                Receive regular updates about new papers matching this project.
            </p>

            <form onSubmit={handleSubmit} className="space-y-5">
                <div className="flex items-center space-x-3">
                    <input
                        type="checkbox"
                        id="newsletter-enable"
                        checked={enabled}
                        onChange={(e) => setEnabled(e.target.checked)}
                        className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 transition-colors"
                    />
                    <label htmlFor="newsletter-enable" className="text-sm font-medium text-gray-700 cursor-pointer select-none">
                        Enable Newsletter
                    </label>
                </div>

                <div className={`space-y-5 transition-opacity duration-300 ${enabled ? 'opacity-100' : 'opacity-50 pointer-events-none'}`}>
                    <div>
                        <label htmlFor="cadence" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                            Frequency
                        </label>
                        <select
                            id="cadence"
                            value={cadence}
                            onChange={(e) => setCadence(e.target.value)}
                            className="w-full bg-white/50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
                        >
                            <option value="Daily">Daily</option>
                            <option value="Weekly">Weekly</option>
                            <option value="Monthly">Monthly</option>
                        </select>
                    </div>

                    {cadence === 'Weekly' && (
                        <div>
                            <label htmlFor="dayOfWeek" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                                Day of Week
                            </label>
                            <select
                                id="dayOfWeek"
                                value={dayOfWeek}
                                onChange={(e) => setDayOfWeek(e.target.value)}
                                className="w-full bg-white/50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
                            >
                                <option value="Monday">Monday</option>
                                <option value="Tuesday">Tuesday</option>
                                <option value="Wednesday">Wednesday</option>
                                <option value="Thursday">Thursday</option>
                                <option value="Friday">Friday</option>
                                <option value="Saturday">Saturday</option>
                                <option value="Sunday">Sunday</option>
                            </select>
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={mutation.isPending}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 flex justify-center items-center disabled:opacity-70 disabled:cursor-not-allowed"
                >
                    {mutation.isPending ? (
                        <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                        'Save Preferences'
                    )}
                </button>

                {/* Status message container - fixed height to prevent layout shifts */}
                <div className="h-12 flex items-center justify-center">
                    <div
                        className={`w-full text-sm p-3 rounded-lg text-center transition-all duration-300 transform ${statusMessage
                                ? `opacity-100 translate-y-0 ${statusMessage.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`
                                : 'opacity-0 translate-y-2 pointer-events-none'
                            }`}
                    >
                        {statusMessage ? statusMessage.text : 'Placeholder'}
                    </div>
                </div>
            </form>
        </div>
    );
}
