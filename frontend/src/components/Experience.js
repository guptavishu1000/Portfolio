import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import api from '../api';

const TimelineItem = ({ title, subtitle, period, location, description, badges = [] }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="relative pl-10"
  >
    <div className="absolute left-0 top-2 w-3 h-3 bg-blue-600 rounded-full" />
    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{title}</h3>
    <div className="text-gray-600 dark:text-gray-300">{subtitle}</div>
    <div className="text-sm text-gray-500 dark:text-gray-400 mb-2">{period}{location ? ` • ${location}` : ''}</div>
    <p className="text-gray-700 dark:text-gray-300 mb-3">{description}</p>
    {Array.isArray(badges) && badges.length > 0 && (
      <div className="flex flex-wrap gap-2">
        {badges.map((b) => (
          <span key={b} className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 text-sm rounded-full">{b}</span>
        ))}
      </div>
    )}
  </motion.div>
);

const Experience = () => {
  const [experience, setExperience] = useState([]);
  const [education, setEducation] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [expRes, eduRes] = await Promise.all([
          api.get('/experience/'),
          api.get('/education/')
        ]);
        
        // Ensure response data is arrays
        const expData = Array.isArray(expRes.data.results) ? expRes.data.results : [];
        const eduData = Array.isArray(eduRes.data.results) ? eduRes.data.results : [];
        
        console.log(eduRes.data.results);

        setExperience(expData);
        setEducation(eduData);
      } catch (error) {
        console.error('Error fetching experience/education:', error);
        setError('Failed to load experience and education data. Please try again later.');
        setExperience([]);
        setEducation([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatDate = (dateStr) => {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", { month: "short", year: "numeric" });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center pt-20 bg-gray-50 dark:bg-gray-900">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h3 className="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-2">Error Loading Data</h3>
            <p className="text-gray-500 dark:text-gray-400 mb-4">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">Experience</h1>
          <p className="text-gray-600 dark:text-gray-300 text-lg">Professional roles and academic background.</p>
        </motion.div>

        {/* Work Experience */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Work</h2>
          <div className="space-y-8 border-l-2 border-gray-200 dark:border-gray-700 pl-6">
            {experience.length === 0 && (
              <div className="text-gray-500 dark:text-gray-400">No experience yet.</div>
            )}
            {experience.map((exp) => (
              <TimelineItem
                key={exp.id}
                title={exp.position}
                subtitle={exp.company}
                period={`${formatDate(exp.start_date)} — ${formatDate(exp.current) ? 'Present' : (formatDate(exp.end_date) || '')}`}
                location={exp.location}
                description={exp.description}
                badges={Array.isArray(exp.technologies_used) ? exp.technologies_used.map(t => t.name) : []}
              />
            ))}
          </div>
        </div>

        {/* Education */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Education</h2>
          <div className="space-y-8 border-l-2 border-gray-200 dark:border-gray-700 pl-6">
            {education.length === 0 && (
              <div className="text-gray-500 dark:text-gray-400">No education yet.</div>
            )}
            {education.map((edu) => (
              <TimelineItem
                key={edu.id}
                title={edu.degree}
                subtitle={`${edu.institution}`}
                period={`${formatDate(edu.start_date)} — ${formatDate(edu.current) ? 'Present' : (formatDate(edu.end_date) || '')}`}
                description={edu.description || ''}
                badges={[]}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Experience;