import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import { GithubIcon, LinkedinIcon, LeetcodeIcon, CodeforcesIcon, KaggleIcon, SocialLink } from './SocialIcons';

const Footer = () => {
  const [personalInfo, setPersonalInfo] = useState(null);

  useEffect(() => {
    const fetchPersonalInfo = async () => {
      try {
        const response = await api.get('/personal-info/current/');
        setPersonalInfo(response.data);
      } catch (error) {
        console.error('Error fetching personal info:', error);
      }
    };

    fetchPersonalInfo();
  }, []);

  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="md:col-span-2">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {personalInfo?.name || 'Portfolio'}
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-md">
              {personalInfo?.bio || 'Passionate developer creating innovative solutions with modern technologies.'}
            </p>
            <div className="flex space-x-4">
              {personalInfo?.github && (
                <SocialLink href={personalInfo.github}>
                  <GithubIcon />
                </SocialLink>
              )}
              
              {personalInfo?.linkedin && (
                <SocialLink href={personalInfo.linkedin}>
                  <LinkedinIcon />
                </SocialLink>
              )}
              
              {personalInfo?.leetcode && (
                <div className="hidden dark:block">
                  <SocialLink href={personalInfo.leetcode}>
                    <LeetcodeIcon darkMode={true} />
                  </SocialLink>
                </div>
              )}
              
              {personalInfo?.leetcode && (
                <div className="dark:hidden">
                  <SocialLink href={personalInfo.leetcode}>
                    <LeetcodeIcon darkMode={false} />
                  </SocialLink>
                </div>
              )}

              {personalInfo?.linkedin && (
                <SocialLink href={personalInfo.linkedin}>
                  <CodeforcesIcon />
                </SocialLink>
              )} 

              {personalInfo?.linkedin && (
                <SocialLink href={personalInfo.linkedin}>
                  <KaggleIcon />
                </SocialLink>
              )} 
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h4>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">
                  About
                </Link>
              </li>
              <li>
                <Link to="/projects" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">
                  Projects
                </Link>
              </li>
              <li>
                <Link to="/experience" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">
                  Experience
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Contact Info</h4>
            <ul className="space-y-3">
              {personalInfo?.email && (
                <li className="flex items-center space-x-3">
                  <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span className="text-gray-600 dark:text-gray-300">{personalInfo.email}</span>
                </li>
              )}
              
              {personalInfo?.phone && (
                <li className="flex items-center space-x-3">
                  <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span className="text-gray-600 dark:text-gray-300">{personalInfo.phone}</span>
                </li>
              )}
              
              {personalInfo?.location && (
                <li className="flex items-center space-x-3">
                  <svg className="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span className="text-gray-600 dark:text-gray-300">{personalInfo.location}</span>
                </li>
              )}
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-200 dark:border-gray-700 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              © {currentYear} {personalInfo?.name || 'Portfolio'}. All rights reserved.
            </p>
            <p className="text-gray-600 dark:text-gray-300 text-sm mt-2 md:mt-0">
              Built with ❤️ using Django & React
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;